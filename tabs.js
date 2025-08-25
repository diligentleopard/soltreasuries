
document.addEventListener("DOMContentLoaded", function () {
  const tabs = document.querySelectorAll(".tab");
  const contents = document.querySelectorAll(".tab-content");

  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      // remove 'active' class from all tabs and content
      tabs.forEach(t => t.classList.remove("active"));
      contents.forEach(c => c.classList.remove("active"));

      // activate the clicked tab and its target content
      tab.classList.add("active");
      const targetId = tab.dataset.target;
      document.getElementById(targetId).classList.add("active");
    });
  });
});
