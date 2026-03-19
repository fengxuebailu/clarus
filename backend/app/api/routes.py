"""
FastAPI Routes for Clarus Go Analysis API
Exposes the War Room functionality via REST endpoints
"""

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import JSONResponse
from typing import List
import json

from ..seminars.war_room import WarRoom
from ..schemas.go_analysis import MoveAnalysis, AnalysisResult
from ..agents.grandmaster import GrandmasterAgent


router = APIRouter(prefix="/api/go", tags=["Go Analysis"])

# Initialize War Room (singleton for this API instance)
war_room = WarRoom()
# Initialize Grandmaster for direct queries
grandmaster = GrandmasterAgent()


@router.post("/analyze", response_model=AnalysisResult)
async def analyze_move(request: Request, analysis: MoveAnalysis):
    """
    Analyze a Go position comparing two moves

    This endpoint runs the complete Reconstruction Game workflow:
    1. KataGo parallel simulation
    2. Delta extraction
    3. Scribe-Profiler-Arbiter loop (max 3 iterations)
    4. Returns validated explanation

    **Example Request:**
    ```json
    {
      "board_state": "(;GM[1]FF[4]SZ[19]...)",
      "move_a": "Q16",
      "move_b": "D4",
      "player_color": "B"
    }
    ```
    """

    # Log incoming request for debugging
    print(f"[API] Received analyze request:")
    print(f"[API]   board_state: {analysis.board_state[:50]}..." if len(analysis.board_state) > 50 else f"[API]   board_state: {analysis.board_state}")
    print(f"[API]   move_a: {analysis.move_a}")
    print(f"[API]   move_b: {analysis.move_b}")
    print(f"[API]   player_color: {analysis.player_color}")

    try:
        result = await war_room.analyze_move(analysis)
        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@router.post("/analyze/batch", response_model=List[AnalysisResult])
async def analyze_batch(
    analyses: List[MoveAnalysis],
    parallel: bool = False
):
    """
    Batch analyze multiple positions

    **Parameters:**
    - `parallel`: If true, run analyses in parallel (faster but more resource-intensive)

    **Example Request:**
    ```json
    [
      {
        "board_state": "(;GM[1]...)",
        "move_a": "Q16",
        "move_b": "D4",
        "player_color": "B"
      },
      {
        "board_state": "(;GM[1]...)",
        "move_a": "D16",
        "move_b": "Q4",
        "player_color": "W"
      }
    ]
    ```
    """

    try:
        results = await war_room.batch_analyze(analyses, parallel=parallel)
        return results

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Batch analysis failed: {str(e)}"
        )


@router.websocket("/ws/analyze")
async def websocket_analyze(websocket: WebSocket):
    """
    WebSocket endpoint for real-time analysis with progress updates

    This allows the frontend to receive updates during the Reconstruction Loop:
    - Scribe generating explanation (T_1, T_2, T_3)
    - Profiler reconstruction attempts
    - Arbiter feedback

    **Message Format:**
    Client sends:
    ```json
    {
      "board_state": "...",
      "move_a": "Q16",
      "move_b": "D4",
      "player_color": "B"
    }
    ```

    Server sends updates:
    ```json
    {
      "type": "progress",
      "stage": "scribe_generating",
      "attempt": 1,
      "message": "Scribe generating explanation T_1..."
    }
    ```

    Final result:
    ```json
    {
      "type": "result",
      "data": { ...AnalysisResult... }
    }
    ```
    """

    await websocket.accept()

    try:
        while True:
            # Receive analysis request
            data = await websocket.receive_text()
            request_data = json.loads(data)

            analysis = MoveAnalysis(**request_data)

            # Send progress updates during analysis
            await websocket.send_json({
                "type": "progress",
                "stage": "started",
                "message": "Starting analysis..."
            })

            # TODO: Integrate progress callbacks into WarRoom
            # For now, just run the analysis
            result = await war_room.analyze_move(analysis)

            # Send final result
            await websocket.send_json({
                "type": "result",
                "data": result.model_dump()
            })

    except WebSocketDisconnect:
        print("[WebSocket] Client disconnected")

    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "message": str(e)
        })
        await websocket.close()


@router.get("/health")
async def health_check():
    """
    Health check endpoint

    Returns system status and agent availability
    """

    return JSONResponse({
        "status": "healthy",
        "agents": {
            "grandmaster": "ready",
            "scribe": "ready",
            "profiler": "ready",
            "arbiter": "ready",
            "delta_hunter": "ready"
        },
        "war_room": "operational"
    })


@router.post("/test")
async def test_endpoint(data: dict):
    """Simple test endpoint"""
    import logging
    logging.info(f"Test endpoint received data: {data}")
    print(f"[TEST] Received data: {data}")
    return {"status": "ok", "received": data}


@router.get("/concepts")
async def get_concept_dictionary():
    """
    Get the current Concept Dictionary

    Returns the vocabulary of Go terms used by the system
    (This would integrate with Seminar II in production)

    For now, returns a basic dictionary
    """

    basic_dictionary = {
        "version": "v1.0",
        "concepts": [
            {
                "concept_name": "Thickness",
                "definition": "Strong, solid formations with outward-facing influence",
                "examples": ["Wall formation", "Ponnuki shape"]
            },
            {
                "concept_name": "Aji",
                "definition": "Latent potential or residual weaknesses in position",
                "examples": ["Cutting points", "Invasion potential"]
            },
            {
                "concept_name": "Shape",
                "definition": "Efficiency and aesthetic quality of stone placement",
                "examples": ["Empty triangle (bad)", "Tiger's mouth (good)"]
            },
            {
                "concept_name": "Sabaki",
                "definition": "Light, flexible maneuvering in difficult situations",
                "examples": ["Light play in opponent's sphere", "Sacrifice tactics"]
            }
        ]
    }

    return JSONResponse(basic_dictionary)


@router.post("/suggest-moves")
async def suggest_moves(request: dict):
    """
    Get AI's recommended moves for the current position

    Returns top 5-10 moves with their evaluations

    **Example Request:**
    ```json
    {
      "board_state": "(;GM[1]FF[4]SZ[19]...)",
      "player_color": "B",
      "num_suggestions": 5
    }
    ```

    **Example Response:**
    ```json
    {
      "suggestions": [
        {
          "move": "Q16",
          "winrate": 0.524,
          "visits": 1500,
          "score_lead": 2.3,
          "rank": 1
        },
        ...
      ]
    }
    ```
    """
    try:
        board_state = request.get("board_state", "(;GM[1]FF[4]SZ[19])")
        player_color = request.get("player_color", "B")
        num_suggestions = request.get("num_suggestions", 5)

        print(f"[API] Getting AI suggestions for {player_color} to play")

        # Get KataGo analysis for current position
        from ..core.katago_client import get_katago_client
        from ..utils.go_board import SGFParser

        # Parse existing moves
        if board_state.startswith("(;"):
            parser = SGFParser(board_state)
            moves = parser.get_moves()
        else:
            moves = []

        # Get KataGo client
        katago = await get_katago_client()

        # Analyze current position with more visits for better move suggestions
        # Note: CPU version of KataGo is much slower, use smaller maxVisits (50 instead of 500)
        result = await katago.analyze(
            moves=moves,
            rules="chinese",
            komi=7.5,
            board_size=19,
            max_visits=50,  # Reduced for CPU performance (was 500)
            include_ownership=True,
            include_policy=True,
            include_pv=True
        )

        # Extract move suggestions from moveInfos
        move_infos = result.get("moveInfos", [])
        suggestions = []

        for i, move_info in enumerate(move_infos[:num_suggestions]):
            suggestions.append({
                "move": move_info.get("move", "pass"),
                "winrate": move_info.get("winrate", 0.5),
                "visits": move_info.get("visits", 0),
                "score_lead": move_info.get("scoreLead", 0.0),
                "rank": i + 1,
                "pv": move_info.get("pv", [])[:5]  # Principal variation (next 5 moves)
            })

        print(f"[API] Found {len(suggestions)} suggestions")

        return JSONResponse({
            "board_state": board_state,
            "player_color": player_color,
            "suggestions": suggestions
        })

    except Exception as e:
        import traceback
        print(f"[API] Error getting suggestions: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/play-move")
async def play_move(request: dict):
    """
    AI plays the best move in current position

    **Example Request:**
    ```json
    {
      "board_state": "(;GM[1]FF[4]SZ[19]...)",
      "player_color": "B"
    }
    ```

    **Example Response:**
    ```json
    {
      "move": "Q16",
      "new_board_state": "(;GM[1]FF[4]SZ[19];B[pd])",
      "winrate": 0.524,
      "score_lead": 2.3,
      "comment": "AI plays Q16 (top-right corner, 4-4 point)"
    }
    ```
    """
    try:
        board_state = request.get("board_state", "(;GM[1]FF[4]SZ[19])")
        player_color = request.get("player_color", "B")

        print(f"[API] AI playing as {player_color}")

        # Get top suggestion
        suggestions_response = await suggest_moves({
            "board_state": board_state,
            "player_color": player_color,
            "num_suggestions": 1
        })

        suggestions_data = json.loads(suggestions_response.body.decode())

        if not suggestions_data.get("suggestions"):
            raise HTTPException(status_code=400, detail="No valid moves available")

        best_move = suggestions_data["suggestions"][0]
        move_str = best_move["move"]

        # Update board state with new move
        from ..utils.go_board import SGFParser

        if board_state.startswith("(;"):
            # Remove closing parenthesis
            new_board_state = board_state.rstrip(")")
            # Add new move
            # Convert move string (like "Q16") to SGF coordinates
            new_board_state += f";{player_color}[{move_to_sgf(move_str)}])"
        else:
            new_board_state = f"(;GM[1]FF[4]SZ[19];{player_color}[{move_to_sgf(move_str)}])"

        return JSONResponse({
            "move": move_str,
            "new_board_state": new_board_state,
            "winrate": best_move["winrate"],
            "score_lead": best_move["score_lead"],
            "comment": f"AI plays {move_str}",
            "pv": best_move.get("pv", [])
        })

    except Exception as e:
        import traceback
        print(f"[API] Error playing move: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


def move_to_sgf(move_str: str) -> str:
    """Convert move string like 'Q16' to SGF format like 'pd'"""
    if move_str.lower() == "pass":
        return ""

    # Extract column (letter) and row (number)
    col = move_str[0].upper()
    row = int(move_str[1:])

    # Convert column: A=a, B=b, ..., skip I, ..., T=s
    col_index = ord(col) - ord('A')
    if col > 'I':  # Skip 'I' in Go notation
        col_index -= 1

    # Convert row: 1=s (bottom), 19=a (top) for standard orientation
    # But SGF uses: 1=a (top), 19=s (bottom)
    row_index = 19 - row

    sgf_col = chr(ord('a') + col_index)
    sgf_row = chr(ord('a') + row_index)

    return f"{sgf_col}{sgf_row}"
