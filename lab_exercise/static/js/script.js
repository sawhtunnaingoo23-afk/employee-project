document.addEventListener("DOMContentLoaded", () => {
    // Mobile navigation
    const toggle = document.querySelector("[data-nav-toggle]");
    const nav = document.querySelector("[data-nav-links]");

    if (toggle && nav) {
        toggle.addEventListener("click", () => {
            const isOpen = nav.classList.toggle("open");
            toggle.setAttribute("aria-expanded", String(isOpen));
        });
    }

    // Live student search
    const search = document.querySelector("[data-student-search]");
    const rows = Array.from(
        document.querySelectorAll("[data-student-row]")
    );
    const visibleCount = document.querySelector("[data-visible-count]");
    const emptySearch = document.querySelector("[data-empty-search]");

    if (search) {
        const updateRows = () => {
            const query = search.value.trim().toLowerCase();
            let visible = 0;

            rows.forEach((row) => {
                const matches = row.textContent
                    .toLowerCase()
                    .includes(query);

                row.hidden = !matches;

                if (matches) visible++;
            });

            if (visibleCount) {
                visibleCount.textContent =
                    `${visible} student${visible === 1 ? "" : "s"} shown`;
            }

            if (emptySearch) {
                emptySearch.hidden = visible !== 0;
            }
        };

        search.addEventListener("input", updateRows);
        updateRows();
    }

    // Student form validation
    const form = document.querySelector("[data-student-form]");

    if (form) {
        const nameInput = form.querySelector('[name="name"]');
        const emailInput = form.querySelector('[name="email"]');

        form.addEventListener("submit", (event) => {
            const name = nameInput.value.trim();
            const email = emailInput.value.trim();

            if (!name || !email) {
                event.preventDefault();
                showToast("Please complete both fields.");

                (!name ? nameInput : emailInput).focus();
                return;
            }

            if (name.length > 100 || email.length > 100) {
                event.preventDefault();
                showToast(
                    "Name and email must be 100 characters or fewer."
                );
                return;
            }

            if (!emailInput.checkValidity()) {
                event.preventDefault();
                showToast("Please enter a valid email address.");
                emailInput.focus();
            }
        });
    }

    // Dismiss notifications
    document.querySelectorAll("[data-dismiss]").forEach((button) => {
        button.addEventListener("click", () => {
            button.closest(".flash")?.remove();
        });
    });

    // Toast notifications
    function showToast(message) {
        let toast = document.querySelector(".toast");

        if (!toast) {
            toast = document.createElement("div");
            toast.className = "toast";
            toast.setAttribute("role", "status");
            document.body.appendChild(toast);
        }

        toast.textContent = message;
        toast.classList.add("show");

        clearTimeout(toast._timer);

        toast._timer = setTimeout(() => {
            toast.classList.remove("show");
        }, 2800);
    }
});

