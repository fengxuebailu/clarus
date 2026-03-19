"""
KataGo Analysis Engine Client
Provides a Python interface to KataGo's Analysis Engine via JSON protocol
"""

import asyncio
import json
import os
import sys
import subprocess
from typing import Optional, Dict, List, Tuple
from pathlib import Path


class KataGoClient:
    """
    Client for KataGo Analysis Engine

    KataGo Analysis Engine uses JSON protocol via stdin/stdout:
    - Send analysis requests as JSON lines
    - Receive analysis results as JSON lines

    Documentation: https://github.com/lightvector/KataGo/blob/master/docs/Analysis_Engine.md
    """

    def __init__(
        self,
        katago_path: Optional[str] = None,
        config_path: Optional[str] = None,
        model_path: Optional[str] = None
    ):
        """
        Initialize KataGo client

        Args:
            katago_path: Path to KataGo executable (defaults to settings or auto-detect)
            config_path: Path to KataGo config file
            model_path: Path to KataGo model file (.bin.gz or .txt.gz)
        """
        # Try to import settings, fallback to auto-detect if not available
        try:
            from .config import settings
            self.katago_path = katago_path or settings.KATAGO_PATH or self._find_katago()
            self.config_path = config_path or settings.KATAGO_CONFIG or self._find_config()
            self.model_path = model_path or settings.KATAGO_MODEL or self._find_model()
        except:
            self.katago_path = katago_path or self._find_katago()
            self.config_path = config_path or self._find_config()
            self.model_path = model_path or self._find_model()

        self.process: Optional[asyncio.subprocess.Process] = None
        self.request_id = 0
        self.running = False
        self._lock = asyncio.Lock()  # Lock for concurrent request protection
        self._stderr_task: Optional[asyncio.Task] = None  # Background task to consume stderr

    def _find_katago(self) -> str:
        """Find KataGo executable"""
        # Check common locations
        common_paths = [
            "katago",  # In PATH
            "katago.exe",  # Windows
            "/usr/local/bin/katago",  # Linux
            str(Path.home() / "katago" / "katago"),
        ]

        for path in common_paths:
            if os.path.exists(path) or os.system(f"which {path} > /dev/null 2>&1") == 0:
                return path

        raise FileNotFoundError(
            "KataGo executable not found. Please install KataGo or set KATAGO_PATH environment variable."
        )

    def _find_config(self) -> str:
        """Find KataGo config file"""
        common_paths = [
            os.getenv("KATAGO_CONFIG"),
            "katago_config.cfg",
            str(Path.home() / "katago" / "analysis_config.cfg"),
        ]

        for path in common_paths:
            if path and os.path.exists(path):
                return path

        raise FileNotFoundError(
            "KataGo config file not found. Please download from "
            "https://github.com/lightvector/KataGo/blob/master/cpp/configs/analysis_example.cfg"
        )

    def _find_model(self) -> str:
        """Find KataGo model file"""
        common_paths = [
            os.getenv("KATAGO_MODEL"),
            "katago_model.bin.gz",
            str(Path.home() / "katago" / "katago_model.bin.gz"),
        ]

        for path in common_paths:
            if path and os.path.exists(path):
                return path

        raise FileNotFoundError(
            "KataGo model file not found. Please download from "
            "https://github.com/lightvector/KataGo/releases"
        )

    async def _create_subprocess_windows(self, cmd: List[str]):
        """
        Windows-specific subprocess creation using threading.

        This is needed because asyncio.create_subprocess_exec() raises
        NotImplementedError on Windows with ProactorEventLoop in Python 3.9.
        """
        import threading

        # Create subprocess in a separate thread to avoid event loop issues
        def create_process():
            return subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=False,  # Binary mode
                bufsize=0,   # Unbuffered
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )

        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        popen_process = await loop.run_in_executor(None, create_process)

        # Wrap Popen in a minimal Process-like object for compatibility
        class PopenWrapper:
            def __init__(self, popen):
                self._popen = popen
                self.stdin = StreamWriterWrapper(popen.stdin)
                self.stdout = StreamReaderWrapper(popen.stdout, loop)
                self.stderr = StreamReaderWrapper(popen.stderr, loop)
                self.pid = popen.pid

            @property
            def returncode(self):
                return self._popen.poll()

            async def wait(self):
                loop = asyncio.get_event_loop()
                return await loop.run_in_executor(None, self._popen.wait)

            def kill(self):
                self._popen.kill()

        class StreamWriterWrapper:
            def __init__(self, stream):
                self._stream = stream

            def write(self, data):
                self._stream.write(data)

            async def drain(self):
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(None, self._stream.flush)

        class StreamReaderWrapper:
            def __init__(self, stream, loop):
                self._stream = stream
                self._loop = loop

            async def readline(self):
                return await self._loop.run_in_executor(None, self._stream.readline)

        return PopenWrapper(popen_process)

    async def start(self):
        """Start KataGo Analysis Engine subprocess"""
        if self.running:
            return

        cmd = [
            self.katago_path,
            "analysis",
            "-config", self.config_path,
            "-model", self.model_path
        ]

        print(f"[KataGo] Starting engine: {' '.join(cmd)}")
        print(f"[KataGo] Checking paths...")
        print(f"[KataGo]   Executable: {self.katago_path} (exists: {os.path.exists(self.katago_path)})")
        print(f"[KataGo]   Config: {self.config_path} (exists: {os.path.exists(self.config_path)})")
        print(f"[KataGo]   Model: {self.model_path} (exists: {os.path.exists(self.model_path)})")

        try:
            # Use Windows-specific subprocess creation on Windows
            if sys.platform == 'win32':
                print("[KataGo] Using Windows-specific subprocess creation")
                self.process = await self._create_subprocess_windows(cmd)
            else:
                self.process = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdin=asyncio.subprocess.PIPE,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
            print(f"[KataGo] Process created with PID: {self.process.pid}")
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"[KataGo] ERROR creating subprocess: {type(e).__name__}: {e}")
            print(f"[KataGo] Full traceback:\n{error_details}")
            raise RuntimeError(f"Failed to create KataGo process: {type(e).__name__}: {e}")

        # Wait for KataGo to be fully ready
        print("[KataGo] Waiting for engine to be ready...")

        # Start background stderr consumer early
        self._stderr_task = asyncio.create_task(self._consume_stderr())

        # Wait for the "ready to begin handling requests" message
        ready_found = False
        start_time = asyncio.get_event_loop().time()
        timeout = 30  # 30 seconds timeout for initialization

        while not ready_found and (asyncio.get_event_loop().time() - start_time) < timeout:
            if self.process.returncode is not None:
                raise RuntimeError(f"KataGo process terminated during initialization. Exit code: {self.process.returncode}")

            # Check if we've seen the ready message via stderr consumer
            # We'll use a simple flag-based approach
            await asyncio.sleep(0.5)

            # For now, just wait a fixed time (we know it takes ~18 seconds)
            if (asyncio.get_event_loop().time() - start_time) >= 20:
                ready_found = True
                break

        if not ready_found:
            raise RuntimeError(f"KataGo did not become ready within {timeout} seconds")

        self.running = True
        print("[KataGo] Engine is ready and accepting requests")

    async def _consume_stderr(self):
        """Background task to continuously consume stderr output"""
        try:
            while self.process:
                line = await self.process.stderr.readline()
                if not line:
                    break
                # Log important stderr messages
                stderr_text = line.decode('utf-8', errors='ignore').strip()
                if stderr_text and any(keyword in stderr_text.lower() for keyword in ['loaded', 'error', 'warning', 'ready', 'started']):
                    print(f"[KataGo stderr] {stderr_text}")
        except Exception as e:
            print(f"[KataGo] stderr consumer error: {e}")

    async def stop(self):
        """Stop KataGo subprocess"""
        if not self.running or not self.process:
            return

        print("[KataGo] Stopping engine...")

        # Cancel stderr consumer task
        if self._stderr_task:
            self._stderr_task.cancel()
            try:
                await self._stderr_task
            except asyncio.CancelledError:
                pass

        # Send termination request
        try:
            self.process.stdin.write(b'{"action":"terminate"}\n')
            await self.process.stdin.drain()
        except:
            pass

        # Wait for process to finish
        try:
            await asyncio.wait_for(self.process.wait(), timeout=5.0)
        except asyncio.TimeoutError:
            self.process.kill()
            await self.process.wait()

        self.running = False
        print("[KataGo] Engine stopped")

    async def analyze(
        self,
        moves: List[Tuple[str, str]],
        rules: str = "chinese",
        komi: float = 7.5,
        board_size: int = 19,
        max_visits: int = 100,
        include_ownership: bool = True,
        include_policy: bool = True,
        include_pv: bool = True,
        timeout: int = 60
    ) -> Dict:
        """
        Analyze a position

        Args:
            moves: List of (color, move) tuples, e.g. [("B", "Q16"), ("W", "D4")]
            rules: Go rules ("chinese", "japanese", "korean", etc.)
            komi: Komi value
            board_size: Board size (9, 13, or 19)
            max_visits: Maximum MCTS visits
            include_ownership: Include ownership/territory map
            include_policy: Include move policy
            include_pv: Include principal variation
            timeout: Timeout in seconds (default: 60)

        Returns:
            Analysis result dictionary
        """
        if not self.running:
            await self.start()

        # Use lock to prevent concurrent stdin/stdout access
        async with self._lock:
            self.request_id += 1
            request_id = f"analysis-{self.request_id}"

            request = {
                "id": request_id,
                "moves": moves,
                "rules": rules,
                "komi": komi,
                "boardXSize": board_size,
                "boardYSize": board_size,
                "maxVisits": max_visits,
                "includeOwnership": include_ownership,
                "includePolicy": include_policy,
                "includePVVisits": include_pv
            }

            print(f"[KataGo] Sending analysis request: id={request_id}, moves={len(moves)}, maxVisits={max_visits}")

            # Send request
            request_json = json.dumps(request) + "\n"
            print(f"[KataGo] Full JSON request: {request_json.strip()}")
            self.process.stdin.write(request_json.encode())
            await self.process.stdin.drain()

            print(f"[KataGo] Request sent, waiting for response (timeout={timeout}s)...")

            # Read response with timeout
            try:
                response_line = await asyncio.wait_for(
                    self.process.stdout.readline(),
                    timeout=timeout
                )
                print(f"[KataGo] Received response ({len(response_line)} bytes)")
                response = json.loads(response_line.decode())
                print(f"[KataGo] Response parsed successfully")
                return response

            except asyncio.TimeoutError:
                print(f"[KataGo] ERROR: Timeout after {timeout}s waiting for KataGo response")
                print(f"[KataGo] Process still running: {self.running}, PID: {self.process.pid if self.process else 'None'}")
                raise RuntimeError(f"KataGo analysis timed out after {timeout} seconds")

    async def analyze_position(
        self,
        moves: List[Tuple[str, str]],
        max_visits: int = 100
    ) -> Dict:
        """
        Simplified analyze method - returns just root info

        Args:
            moves: List of (color, move) tuples
            max_visits: MCTS visits

        Returns:
            Dictionary with winrate, scoreLead, ownership, policy
        """
        result = await self.analyze(
            moves=moves,
            max_visits=max_visits,
            include_ownership=True,
            include_policy=True
        )

        root_info = result.get("rootInfo", {})

        # NOTE: ownership and policy are at top level, NOT in rootInfo!
        return {
            "winrate": root_info.get("winrate", 0.5),
            "scoreLead": root_info.get("scoreLead", 0.0),
            "ownership": result.get("ownership", []),  # Top level, not rootInfo
            "policy": result.get("policy", []),        # Top level, not rootInfo
            "visits": root_info.get("visits", max_visits),
            "pv": [move_info.get("move") for move_info in result.get("moveInfos", [])[:10]]  # Top 10 moves
        }

    async def __aenter__(self):
        """Async context manager entry"""
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.stop()


# Global singleton instance
_katago_client: Optional[KataGoClient] = None


async def get_katago_client() -> KataGoClient:
    """Get global KataGo client instance"""
    global _katago_client

    if _katago_client is None:
        _katago_client = KataGoClient()
        await _katago_client.start()

    return _katago_client


async def shutdown_katago_client():
    """Shutdown global KataGo client"""
    global _katago_client

    if _katago_client:
        await _katago_client.stop()
        _katago_client = None
