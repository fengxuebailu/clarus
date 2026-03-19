// Particle System
function createParticles() {
    const particlesContainer = document.getElementById('particles');
    const particleCount = 30;

    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';

        // Random horizontal position
        const startX = Math.random() * 100;
        const drift = (Math.random() - 0.5) * 200; // Random drift -100 to 100

        particle.style.left = `${startX}%`;
        particle.style.setProperty('--drift', `${drift}px`);

        // Random delay for staggered animation
        particle.style.animationDelay = `${Math.random() * 15}s`;

        // Random size variation
        const size = 2 + Math.random() * 3;
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;

        particlesContainer.appendChild(particle);
    }
}

// Initialize particles on load
createParticles();

// Interactive Go Board
const board = document.querySelector('.go-board');
const svg = document.querySelector('.board-grid');
const stonesGroup = document.querySelector('.stones');

let currentPlayer = 'black'; // 'black' or 'white'

// Add click handler to board
svg.addEventListener('click', (e) => {
    const rect = svg.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    // Convert to board coordinates (assuming 400x400 viewBox)
    const boardX = (x / rect.width) * 400;
    const boardY = (y / rect.height) * 400;

    // Snap to nearest grid intersection (20px spacing, starting at 20px offset)
    const gridX = Math.round((boardX - 20) / 20) * 20 + 20;
    const gridY = Math.round((boardY - 20) / 20) * 20 + 20;

    // Check if position is valid (within board bounds)
    if (gridX >= 20 && gridX <= 380 && gridY >= 20 && gridY <= 380) {
        placeStone(gridX, gridY, currentPlayer);
        currentPlayer = currentPlayer === 'black' ? 'white' : 'black';
    }
});

function placeStone(x, y, color) {
    // Check if stone already exists at this position
    const existingStones = stonesGroup.querySelectorAll('circle');
    for (let stone of existingStones) {
        const cx = parseFloat(stone.getAttribute('cx'));
        const cy = parseFloat(stone.getAttribute('cy'));
        if (Math.abs(cx - x) < 5 && Math.abs(cy - y) < 5) {
            return; // Position occupied
        }
    }

    // Create new stone
    const stone = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    stone.setAttribute('cx', x);
    stone.setAttribute('cy', y);
    stone.setAttribute('r', 8);
    stone.setAttribute('class', 'stone');
    stone.setAttribute('filter', 'url(#glow)');

    if (color === 'black') {
        stone.setAttribute('fill', '#1a1a1a');
    } else {
        stone.setAttribute('fill', '#f8f8f8');
        stone.setAttribute('stroke', '#ddd');
        stone.setAttribute('stroke-width', '0.5');
    }

    stonesGroup.appendChild(stone);

    // Play placement sound (visual feedback)
    animateStonePlace(stone);
}

function animateStonePlace(stone) {
    // Create ripple effect
    const cx = stone.getAttribute('cx');
    const cy = stone.getAttribute('cy');

    const ripple = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    ripple.setAttribute('cx', cx);
    ripple.setAttribute('cy', cy);
    ripple.setAttribute('r', 8);
    ripple.setAttribute('fill', 'none');
    ripple.setAttribute('stroke', 'rgba(212, 175, 55, 0.8)');
    ripple.setAttribute('stroke-width', '2');

    stonesGroup.appendChild(ripple);

    // Animate ripple
    let radius = 8;
    let opacity = 0.8;
    const animate = () => {
        radius += 1.5;
        opacity -= 0.05;

        ripple.setAttribute('r', radius);
        ripple.setAttribute('stroke-opacity', opacity);

        if (opacity > 0) {
            requestAnimationFrame(animate);
        } else {
            ripple.remove();
        }
    };

    requestAnimationFrame(animate);
}

// Close button functionality
const closeBtn = document.querySelector('.close-btn');
closeBtn.addEventListener('click', () => {
    // Add closing animation
    document.querySelector('.main-container').style.animation = 'platformRise 0.5s ease-in reverse';

    setTimeout(() => {
        // In a real app, this would close the modal/page
        alert('游戏界面已关闭');
        location.reload();
    }, 500);
});

// Start button functionality
const startBtn = document.querySelector('.start-btn');
startBtn.addEventListener('click', () => {
    // Add click effect
    startBtn.style.transform = 'translateX(-50%) scale(0.95)';

    setTimeout(() => {
        startBtn.style.transform = 'translateX(-50%) scale(1)';
    }, 100);

    // Clear existing stones for new game
    setTimeout(() => {
        const confirmation = confirm('开始新对弈？当前棋局将被清空。');
        if (confirmation) {
            // Remove all stones except highlighted ones (keep them as decoration)
            const allStones = stonesGroup.querySelectorAll('circle:not(.highlight-stone)');
            allStones.forEach((stone, index) => {
                setTimeout(() => {
                    stone.style.animation = 'stoneDrop 0.3s ease-in reverse';
                    setTimeout(() => stone.remove(), 300);
                }, index * 30);
            });

            currentPlayer = 'black';

            // Show ready message
            setTimeout(() => {
                showMessage('对弈开始！黑方先行');
            }, allStones.length * 30 + 300);
        }
    }, 150);
});

// Message display function
function showMessage(text) {
    const message = document.createElement('div');
    message.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        padding: 20px 40px;
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.95), rgba(244, 208, 63, 0.95));
        border: 3px solid rgba(255, 255, 255, 0.5);
        border-radius: 50px;
        color: #1a1a1a;
        font-size: 24px;
        font-weight: 900;
        font-family: 'ZCOOL XiaoWei', 'Noto Serif SC', sans-serif;
        letter-spacing: 4px;
        z-index: 1000;
        box-shadow: 0 0 40px rgba(212, 175, 55, 0.8), 0 10px 30px rgba(0, 0, 0, 0.5);
        animation: messageAppear 0.5s ease-out;
    `;
    message.textContent = text;

    document.body.appendChild(message);

    setTimeout(() => {
        message.style.animation = 'messageAppear 0.5s ease-in reverse';
        setTimeout(() => message.remove(), 500);
    }, 2000);
}

// Add message animation to stylesheet dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes messageAppear {
        from {
            opacity: 0;
            transform: translate(-50%, -50%) scale(0.8);
        }
        to {
            opacity: 1;
            transform: translate(-50%, -50%) scale(1);
        }
    }
`;
document.head.appendChild(style);

// Hover effects for stones
svg.addEventListener('mousemove', (e) => {
    const rect = svg.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const boardX = (x / rect.width) * 400;
    const boardY = (y / rect.height) * 400;

    const gridX = Math.round((boardX - 20) / 20) * 20 + 20;
    const gridY = Math.round((boardY - 20) / 20) * 20 + 20;

    // Remove previous preview
    const oldPreview = document.querySelector('.stone-preview');
    if (oldPreview) oldPreview.remove();

    // Show preview stone if valid position
    if (gridX >= 20 && gridX <= 380 && gridY >= 20 && gridY <= 380) {
        // Check if position is empty
        const existingStones = stonesGroup.querySelectorAll('circle');
        let isEmpty = true;
        for (let stone of existingStones) {
            const cx = parseFloat(stone.getAttribute('cx'));
            const cy = parseFloat(stone.getAttribute('cy'));
            if (Math.abs(cx - gridX) < 5 && Math.abs(cy - gridY) < 5) {
                isEmpty = false;
                break;
            }
        }

        if (isEmpty) {
            const preview = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
            preview.setAttribute('cx', gridX);
            preview.setAttribute('cy', gridY);
            preview.setAttribute('r', 8);
            preview.setAttribute('class', 'stone-preview');
            preview.setAttribute('opacity', '0.4');

            if (currentPlayer === 'black') {
                preview.setAttribute('fill', '#1a1a1a');
            } else {
                preview.setAttribute('fill', '#f8f8f8');
                preview.setAttribute('stroke', '#ddd');
                preview.setAttribute('stroke-width', '0.5');
            }

            stonesGroup.appendChild(preview);
        }
    }
});

svg.addEventListener('mouseleave', () => {
    const preview = document.querySelector('.stone-preview');
    if (preview) preview.remove();
});

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeBtn.click();
    }

    if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        startBtn.click();
    }

    // Clear board with 'C' key
    if (e.key === 'c' || e.key === 'C') {
        const allStones = stonesGroup.querySelectorAll('circle:not(.highlight-stone)');
        allStones.forEach((stone, index) => {
            setTimeout(() => {
                stone.style.animation = 'stoneDrop 0.3s ease-in reverse';
                setTimeout(() => stone.remove(), 300);
            }, index * 20);
        });
        currentPlayer = 'black';
        showMessage('棋盘已清空');
    }
});

// Add ambient sound trigger (visual only - no actual audio)
let ambientActive = false;
document.addEventListener('click', () => {
    if (!ambientActive) {
        ambientActive = true;
        // Could trigger ambient sounds here in a full implementation
        console.log('🎵 Ambient atmosphere activated');
    }
});

// Performance optimization: Reduce particles on mobile
if (window.innerWidth < 768) {
    const particles = document.querySelectorAll('.particle');
    particles.forEach((particle, index) => {
        if (index > 15) particle.remove();
    });
}

// Add loading complete animation
window.addEventListener('load', () => {
    document.body.style.opacity = '1';
    console.log('🎮 围棋·段位提升 - Interface loaded successfully');
});

// Initial setup
document.body.style.opacity = '0';
document.body.style.transition = 'opacity 0.5s ease-in';

console.log('🎮 围棋·段位提升');
console.log('⚫ 黑方先行');
console.log('快捷键: ESC=关闭 | ENTER=开始 | C=清空棋盘');
