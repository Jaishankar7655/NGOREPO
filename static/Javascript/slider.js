const slides = document.querySelectorAll(".slide");
      const navBtns = document.querySelector(".navigation");
      const leftArrow = document.querySelector(".arrow-left");
      const rightArrow = document.querySelector(".arrow-right");
      const progressBar = document.querySelector(".progress-bar");
      let currentSlide = 0;
      let autoSlideInterval;
      const autoSlideDuration = 5000; // 5 seconds

      // Create navigation buttons
      slides.forEach((_, index) => {
        const btn = document.createElement("div");
        btn.classList.add("nav-btn");
        if (index === 0) btn.classList.add("active");
        btn.addEventListener("click", () => goToSlide(index));
        navBtns.appendChild(btn);
      });

      function goToSlide(n) {
        slides[currentSlide].classList.remove("active");
        navBtns.children[currentSlide].classList.remove("active");
        currentSlide = (n + slides.length) % slides.length;
        slides[currentSlide].classList.add("active");
        navBtns.children[currentSlide].classList.add("active");
        resetAutoSlide();
        updateProgressBar();
      }

      function nextSlide() {
        goToSlide(currentSlide + 1);
      }

      function prevSlide() {
        goToSlide(currentSlide - 1);
      }

      function startAutoSlide() {
        autoSlideInterval = setInterval(nextSlide, autoSlideDuration);
        updateProgressBar();
      }

      function resetAutoSlide() {
        clearInterval(autoSlideInterval);
        progressBar.style.width = "0";
        startAutoSlide();
      }

      function updateProgressBar() {
        let width = 0;
        const intervalDuration = 50; // Update every 50ms for smooth animation
        const increment = (intervalDuration / autoSlideDuration) * 100;

        const progressInterval = setInterval(() => {
          width += increment;
          progressBar.style.width = `${width}%`;

          if (width >= 100) {
            clearInterval(progressInterval);
          }
        }, intervalDuration);
      }

      leftArrow.addEventListener("click", prevSlide);
      rightArrow.addEventListener("click", nextSlide);

      document
        .querySelector(".slider-container")
        .addEventListener("mouseover", () => {
          clearInterval(autoSlideInterval);
          progressBar.style.width = "0";
        });

      document
        .querySelector(".slider-container")
        .addEventListener("mouseout", resetAutoSlide);

      // Keyboard navigation
      document.addEventListener("keydown", (e) => {
        if (e.key === "ArrowLeft") prevSlide();
        if (e.key === "ArrowRight") nextSlide();
      });

      // Touch swipe functionality
      let touchStartX = 0;
      let touchEndX = 0;

      document
        .querySelector(".slider-container")
        .addEventListener("touchstart", (e) => {
          touchStartX = e.changedTouches[0].screenX;
        });

      document
        .querySelector(".slider-container")
        .addEventListener("touchend", (e) => {
          touchEndX = e.changedTouches[0].screenX;
          handleSwipe();
        });

      function handleSwipe() {
        if (touchEndX < touchStartX) nextSlide();
        if (touchEndX > touchStartX) prevSlide();
      }

      // Start auto-sliding
      startAutoSlide();