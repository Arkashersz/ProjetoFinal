document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");

  form.addEventListener("submit", function (event) {
    const emailInput = form.querySelector('input[name="email"]');
    const passwordInput = form.querySelector('input[name="password"]');
    const emailError = document.getElementById("email-error");
    const passwordError = document.getElementById("password-error");

    // Limpa mensagens de erro anteriores
    emailError.textContent = "";
    passwordError.textContent = "";

    // Validação do e-mail
    if (!is_valid_email(emailInput.value)) {
      emailError.textContent = "E-mail inválido.";
      event.preventDefault();
    }

    // Validação da senha
    if (!is_valid_password(passwordInput.value)) {
      passwordError.textContent =
        "A senha deve ter pelo menos 5 caracteres e conter pelo menos uma letra.";
      event.preventDefault();
    }
  });
});
