// Small script for alerts and interactions
document.addEventListener("DOMContentLoaded", () => {
  console.log("📚 Library Dashboard Loaded!");

  // Highlight active nav item (if future pages added)
  const currentPath = window.location.pathname;
  document.querySelectorAll(".navbar-nav a").forEach(link => {
    if (link.getAttribute("href") === currentPath) {
      link.classList.add("active");
    }
  });

  // Handle flash messages (success/error)
  const flashMessages = document.querySelectorAll(".alert");
  flashMessages.forEach(msg => {
    // Show the message for 4 seconds then hide
    setTimeout(() => {
      msg.style.display = "none";
    }, 4000); 
  });

  // Example: dynamically show a toast for registration or login success
  const showToast = (message, type="success") => {
    const toast = document.createElement("div");
    toast.className = `alert alert-${type}`;
    toast.style.position = "fixed";
    toast.style.top = "20px";
    toast.style.right = "20px";
    toast.style.zIndex = "9999";
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
      toast.remove();
    }, 4000);
  };

  // Check if there's a data attribute on body for flash message
  const bodyMsg = document.body.getAttribute("data-flash");
  if(bodyMsg) {
    showToast(bodyMsg, "success");
  }
});
