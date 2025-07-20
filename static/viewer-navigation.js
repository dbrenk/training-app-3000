// viewer-navigation.js

document.addEventListener('keydown', function(event) {
    if (event.key === 'ArrowLeft') {
        window.location.href = `/viewer?set=${setName}&index=${previousIndex}`;
    } else if (event.key === 'ArrowRight') {
        window.location.href = `/viewer?set=${setName}&index=${nextIndex}`;
    }
});

let touchStartX = 0;
let touchEndX = 0;

function handleGesture() {
    if (touchEndX < touchStartX - 50) {
        window.location.href = `/viewer?set=${setName}&index=${nextIndex}`;
    }
    if (touchEndX > touchStartX + 50) {
        window.location.href = `/viewer?set=${setName}&index=${previousIndex}`;
    }
}

document.addEventListener('touchstart', e => {
    touchStartX = e.changedTouches[0].screenX;
});

document.addEventListener('touchend', e => {
    touchEndX = e.changedTouches[0].screenX;
    handleGesture();
});

// === ENTER KEY TOGGLE AUDIO PLAY/PAUSE WHEN VISIBLE ===

const audioElement = document.getElementById('play-btn');
let audioVisible = false;

if (audioElement) {
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach(entry => {
                audioVisible = entry.isIntersecting;
            });
        },
        { threshold: 0.5 }
    );

    observer.observe(audioElement);

    document.addEventListener('keydown', function(event) {
        if (event.key === 'Enter' && audioVisible) {
            if (audioElement.paused) {
                audioElement.play();
            } else {
                audioElement.pause();
            }
        }
    });
}
