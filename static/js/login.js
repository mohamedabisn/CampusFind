document.addEventListener("DOMContentLoaded", () => {
  const tabs = document.querySelectorAll(".auth-tab, .inline-switch");
  const login = document.getElementById("loginForm");
  const register = document.getElementById("registerForm");
  const title = document.getElementById("authTitle");
  const subtitle = document.getElementById("authSubtitle");
  function setMode(mode) {
    const reg = mode === "register";
    login.classList.toggle("hidden", reg);
    register.classList.toggle("hidden", !reg);
    document.querySelectorAll(".auth-tab").forEach(b => b.classList.toggle("active", b.dataset.mode === mode));
    title.textContent = reg ? "Create your account" : "Sign in";
    subtitle.textContent = reg ? "Set up your campus profile in less than a minute." : "Use your CampusFind account to continue.";
    history.replaceState({}, "", `/login?mode=${mode}`);
  }
  tabs.forEach(b => b.addEventListener("click", () => setMode(b.dataset.mode)));
  document.querySelectorAll(".show-pass").forEach(btn => btn.addEventListener("click", () => {
    const input = btn.parentElement.querySelector("input");
    input.type = input.type === "password" ? "text" : "password";
    btn.textContent = input.type === "password" ? "Show" : "Hide";
  }));
});
