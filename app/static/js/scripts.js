
 // GSAP Animation for Navbar
 gsap.from(".navbar", {
    duration: 1,
    y: -50,
    opacity: 0,
    ease: "power2.out"
});

// GSAP Animation for Nav Links
gsap.from(".nav-item", {
    duration: 1,
    x: -50,
    opacity: 0,
    stagger: 0.2,
    delay: 0.5,
    ease: "power2.out"
});

// GSAP Animation for Dropdown
document.querySelectorAll('.dropdown-toggle').forEach(item => {
    item.addEventListener('click', () => {
        gsap.from('.dropdown-menu', {
            duration: 0.5,
            y: -20,
            opacity: 0,
            ease: "power2.out"
        });
    });
});

// GSAP Animation for Core Values
document.addEventListener('DOMContentLoaded', function() {
    gsap.from(".core-value", {
        duration: 1,
        opacity: 0,
        y: 50,
        stagger: 0.3
    });
});

document.addEventListener('DOMContentLoaded', function() {
    gsap.from(".container", { duration: 1, opacity: 0, y: -50 });
    gsap.from("h1, h2", { duration: 1, opacity: 0, x: -50, stagger: 0.1 });
    // gsap.from("p, ul, a", { duration: 1, opacity: 0, y: 50, stagger: 0.1 });
});

document.addEventListener('DOMContentLoaded', function() {
    gsap.registerPlugin(ScrollTrigger);

    gsap.from('.core-value-card', {
        scrollTrigger: {
            trigger: '.core-value-card',
            start: 'top 80%',
            toggleActions: 'play none none none'
        },
        opacity: 0,
        y: 50,
        duration: 1
    });
});

// importance of precision oncology cards

document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.hoverable-card .card-body');
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = 1;
        }
      });
    }, { threshold: 0.1 });

    cards.forEach(card => {
      observer.observe(card);
    });
  });