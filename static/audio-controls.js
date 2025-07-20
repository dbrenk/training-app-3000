
// audio-controls.js

// Ensure Howler.js is loaded before this script
// Example: <script src="https://cdnjs.cloudflare.com/ajax/libs/howler/2.2.4/howler.min.js"></script>

document.addEventListener('DOMContentLoaded', function () {
  const audioSrc = window.audioSource || ''; // Set this variable in your HTML before loading this script
  if (!audioSrc) {
    console.warn('No audio source provided for Howler.js');
    return;
  }

  const sound = new Howl({
    src: [audioSrc],
    html5: true
  });

  let isPlaying = false;

  // Optional: attach to buttons if they exist
  const playBtn = document.getElementById('play-btn');
  const pauseBtn = document.getElementById('pause-btn');

  if (playBtn) {
    playBtn.addEventListener('click', () => {
      sound.play();
      isPlaying = true;
    });
  }

  if (pauseBtn) {
    pauseBtn.addEventListener('click', () => {
      sound.pause();
      isPlaying = false;
    });
  }

  // Track visibility of audio container
  let audioVisible = false;
  const audioContainer = document.getElementById('audio-container');

  if (audioContainer) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          audioVisible = entry.isIntersecting;
        });
      },
      { threshold: 0.5 }
    );
    observer.observe(audioContainer);
  }

  // Keyboard controls: Enter or Space toggles play/pause
  document.addEventListener('keydown', function (event) {
    if (!audioVisible) return;
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      if (isPlaying) {
        sound.pause();
      } else {
        sound.play();
      }
      isPlaying = !isPlaying;
    }
  });
});
