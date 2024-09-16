const allinks = document.querySelectorAll("a:link");

allinks.forEach(function (link) {
  link.addEventListener("click", function (event) {
    event.preventDefault();
    const href = link.getAttribute("href");

    if (href === "#")
      window.scrollTo({
        behavior: "smooth",
        top: 0,
      });

    if (href !== "#" && href.startsWith("#")) {
      const sectionEl = document.querySelector(href);
      sectionEl.scrollIntoView({ behavior: "smooth" });
      console.log(sectionEl);
    }
  });
});


const sectionHero = document.querySelector(".section-hero");

const obs = new IntersectionObserver(
  function(entries) {
    const ent = entries[0];
    if(ent.isIntersecting == false){
      document.body.classList.add("sticky");
    }
    if(ent.isIntersecting == true){
      document.body.classList.remove("sticky");
    }
  },{
    root: null,
    threshold: 0,
    rootMargin:"-80px",
  }
)

obs.observe(sectionHero);

const btnNav = document.querySelector(".btn-mobile-nav");
const headerel = document.querySelector(".header");
btnNav.addEventListener("click",function () {
        headerel.classList.toggle('nav-open')
});

