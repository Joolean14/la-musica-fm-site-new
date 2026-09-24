/* JavaScript progresivo: si algo de esto falla, la navegación, la lectura y el
   formulario siguen funcionando con HTML nativo. */

(function () {
  "use strict";

  /* ---------- Menú móvil ---------- */

  function setupMobileMenu() {
    var button = document.querySelector("[data-menu-button]");
    var panel = document.querySelector("[data-mobile-nav]");
    if (!button || !panel) return;

    function setOpen(isOpen) {
      panel.setAttribute("data-open", String(isOpen));
      button.setAttribute("aria-expanded", String(isOpen));
      button.querySelector(".visually-hidden").textContent = isOpen ? "Cerrar menú" : "Abrir menú";
      if (isOpen) {
        var firstLink = panel.querySelector("a");
        if (firstLink) firstLink.focus();
      }
    }

    button.addEventListener("click", function () {
      setOpen(button.getAttribute("aria-expanded") !== "true");
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && button.getAttribute("aria-expanded") === "true") {
        setOpen(false);
        button.focus();
      }
    });
  }

  /* ---------- Filtros del mapa de conexiones ---------- */

  function setupMapFilters() {
    var buttons = document.querySelectorAll("[data-map-filter]");
    if (!buttons.length) return;
    var items = document.querySelectorAll("[data-map-item]");

    buttons.forEach(function (button) {
      button.addEventListener("click", function () {
        var selected = button.getAttribute("data-map-filter");
        buttons.forEach(function (other) {
          other.setAttribute("aria-pressed", String(other === button));
        });
        items.forEach(function (item) {
          var kind = item.getAttribute("data-kind") || "";
          item.hidden = selected !== "todos" && kind.indexOf(selected) === -1;
        });
      });
    });
  }

  /* ---------- Contexto precargado en el formulario ---------- */

  var CONTEXT_KEYS = ["need", "family", "service", "route"];

  function readContextFromUrl() {
    var params = new URLSearchParams(window.location.search);
    var context = {};
    CONTEXT_KEYS.forEach(function (key) {
      var value = params.get(key);
      if (value) context[key] = value;
    });
    return context;
  }

  function applyContext(form, context) {
    CONTEXT_KEYS.forEach(function (key) {
      var hidden = form.querySelector('[data-context-field="' + key + '"]');
      if (hidden && context[key]) hidden.value = context[key];
    });

    if (context.need) {
      var option = form.querySelector('input[name="need"][value="' + CSS.escape(context.need) + '"]');
      if (option) option.checked = true;
    }

    var note = document.querySelector("[data-context-note]");
    if (!note) return;
    var parts = [];
    if (context.service) parts.push("servicio: " + context.service);
    else if (context.family) parts.push("familia: " + context.family);
    if (context.route) parts.push("ruta: " + context.route);
    if (!parts.length) return;
    note.textContent = "Traemos tu selección — " + parts.join(" · ") + ". Puedes cambiarla abajo.";
    note.hidden = false;
  }

  /* ---------- Validación y envío ---------- */

  function clearErrors(form) {
    form.querySelectorAll(".field-error").forEach(function (node) { node.textContent = ""; });
    form.querySelectorAll("[aria-invalid]").forEach(function (node) { node.removeAttribute("aria-invalid"); });
  }

  function showErrors(form, invalidControls) {
    var summary = form.querySelector("[data-form-summary]");
    invalidControls.forEach(function (control) {
      control.setAttribute("aria-invalid", "true");
      var message = form.querySelector('[data-error-for="' + control.name + '"]');
      if (message && !message.textContent) {
        message.textContent = control.validationMessage || "Revisa este campo.";
      }
    });
    if (summary) {
      summary.textContent = "Faltan " + invalidControls.length + " campos por completar o corregir.";
      summary.hidden = false;
      summary.focus();
    }
    if (invalidControls[0]) invalidControls[0].focus();
  }

  function setupContactForm() {
    var form = document.querySelector("[data-contact-form]");
    if (!form) return;

    applyContext(form, readContextFromUrl());

    var status = form.querySelector("[data-form-status]");
    var submitButton = form.querySelector('button[type="submit"]');

    form.addEventListener("submit", function (event) {
      clearErrors(form);
      var summary = form.querySelector("[data-form-summary]");
      if (summary) summary.hidden = true;

      var invalid = Array.prototype.filter.call(form.elements, function (control) {
        return control.willValidate && !control.checkValidity();
      });
      if (invalid.length) {
        event.preventDefault();
        showErrors(form, invalid);
        return;
      }

      // Envío asíncrono cuando el navegador lo permite; si falla, el POST normal sigue disponible.
      if (!window.fetch) return;
      event.preventDefault();
      submitButton.disabled = true;
      status.dataset.state = "sending";
      status.textContent = "Enviando…";

      fetch(form.action, { method: "POST", body: new FormData(form), headers: { Accept: "application/json" } })
        .then(function (response) {
          if (!response.ok) throw new Error("respuesta " + response.status);
          form.reset();
          status.dataset.state = "success";
          status.textContent = status.dataset.successMessage;
        })
        .catch(function () {
          status.dataset.state = "error";
          status.textContent = "No pudimos enviar el formulario. Intenta de nuevo o escríbenos por otro canal.";
        })
        .finally(function () { submitButton.disabled = false; });
    });
  }

  /* ---------- Búsqueda básica del blog ---------- */

  function setupPostSearch() {
    var input = document.querySelector("[data-post-search]");
    if (!input) return;
    var cards = document.querySelectorAll("[data-post-card]");
    var counter = document.querySelector("[data-post-count]");

    input.addEventListener("input", function () {
      var query = input.value.trim().toLowerCase();
      var visible = 0;
      cards.forEach(function (card) {
        var haystack = card.getAttribute("data-search") || "";
        var matches = !query || haystack.indexOf(query) !== -1;
        card.hidden = !matches;
        if (matches) visible += 1;
      });
      if (counter) counter.textContent = visible + " artículos";
    });
  }

  setupMobileMenu();
  setupMapFilters();
  setupContactForm();
  setupPostSearch();
})();
