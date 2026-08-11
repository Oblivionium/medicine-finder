const themeToggle = document.getElementById(
    "theme-toggle"
);

const savedTheme = localStorage.getItem(
    "theme"
);

const initialTheme =
    savedTheme || "dark";

document.documentElement.dataset.theme =
    initialTheme;

themeToggle.textContent =
    initialTheme === "dark"
        ? "☀"
        : "☾";


themeToggle.addEventListener(
    "click",
    () => {

        const currentTheme =
            document.documentElement.dataset.theme;

        const newTheme =
            currentTheme === "dark"
                ? "light"
                : "dark";

        document.documentElement.dataset.theme =
            newTheme;

        localStorage.setItem(
            "theme",
            newTheme
        );

        themeToggle.textContent =
            newTheme === "dark"
                ? "☀"
                : "☾";
    }
);

const searchInput = document.getElementById(
    "medicine-search"
);

const searchResults = document.getElementById(
    "search-results"
);

const medicineDetails = document.getElementById(
    "medicine-details"
);

const selectedMedicine = document.getElementById(
    "selected-medicine"
);

const medicineInfo = document.getElementById(
    "medicine-info"
);

const predictButton = document.getElementById(
    "predict-button"
);

const predictionResult = document.getElementById(
    "prediction-result"
);

const alternativesSection = document.getElementById(
    "alternatives-section"
);

const alternativeResult = document.getElementById(
    "alternative-result"
);


let selectedMedicineName = null;

let searchTimeout = null;


searchInput.addEventListener(
    "input",
    () => {

        clearTimeout(searchTimeout);

        const query = searchInput.value.trim();

        if (!query) {
            searchResults.innerHTML = "";
            return;
        }

        searchTimeout = setTimeout(
            () => searchMedicines(query),
            250
        );
    }
);


async function searchMedicines(query) {

    searchResults.innerHTML = "Searching...";

    try {

        const response = await fetch(
            `/api/search?query=${encodeURIComponent(query)}`
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Search failed"
            );
        }

        if (data.results.length === 0) {

            searchResults.innerHTML = `
                <div class="result">
                    No medicines found.
                </div>
            `;

            return;
        }


        searchResults.innerHTML =
            data.results
                .map(
                    (medicine) => `
                        <button
                            class="medicine-option"
                            data-name="${escapeHtml(
                                medicine.brand_name
                            )}"
                        >
                            <strong>
                                ${escapeHtml(
                                    medicine.brand_name
                                )}
                            </strong>

                            <span>
                                ${escapeHtml(
                                    medicine.manufacturer
                                )}
                            </span>

                            <span>
                                ${escapeHtml(
                                    medicine.primary_strength ||
                                    ""
                                )}
                            </span>
                        </button>
                    `
                )
                .join("");


        document
            .querySelectorAll(".medicine-option")
            .forEach(
                (button) => {

                    button.addEventListener(
                        "click",
                        () => {

                            selectMedicine(
                                button.dataset.name
                            );
                        }
                    );
                }
            );

    } catch (error) {

        searchResults.innerHTML = `
            <div class="error">
                ${error.message}
            </div>
        `;
    }
}


async function selectMedicine(medicineName) {

    selectedMedicineName = medicineName;

    searchInput.value = medicineName;

    searchResults.innerHTML = "";

    medicineDetails.style.display = "block";

    alternativesSection.style.display = "none";

    predictionResult.innerHTML = "";

    alternativeResult.innerHTML = "";

    selectedMedicine.textContent = medicineName;

    medicineInfo.innerHTML = `
        <p>
            Selected medicine:
            <strong>${escapeHtml(medicineName)}</strong>
        </p>
    `;
}


predictButton.addEventListener(
    "click",
    async () => {

        if (!selectedMedicineName) {
            return;
        }

        predictionResult.innerHTML =
            "Predicting price...";

        try {

            const response = await fetch(
                `/api/predict/${encodeURIComponent(
                    selectedMedicineName
                )}`
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.detail || "Prediction failed"
                );
            }

            predictionResult.innerHTML = `
                <div class="result">
                    Predicted Price:
                    <strong>
                        ₹${data.predicted_price.toFixed(2)}
                    </strong>
                </div>
            `;

            await loadAlternatives();

        } catch (error) {

            predictionResult.innerHTML = `
                <div class="error">
                    ${error.message}
                </div>
            `;
        }
    }
);


async function loadAlternatives() {

    alternativesSection.style.display = "block";

    alternativeResult.innerHTML =
        "Finding alternatives...";

    try {

        const response = await fetch(
            `/api/alternatives/${encodeURIComponent(
                selectedMedicineName
            )}`
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Could not find alternatives"
            );
        }

        const alternatives = data.alternatives;

        if (alternatives.length === 0) {

            alternativeResult.innerHTML = `
                <div class="result">
                    No alternatives found.
                </div>
            `;

            return;
        }


        alternativeResult.innerHTML = `
            <table>
                <thead>
                    <tr>
                        <th>Medicine</th>
                        <th>Manufacturer</th>
                        <th>Price</th>
                    </tr>
                </thead>

                <tbody>
                    ${
                        alternatives
                            .map(
                                (medicine) => `
                                    <tr>
                                        <td>
                                            ${escapeHtml(
                                                medicine.brand_name
                                            )}
                                        </td>

                                        <td>
                                            ${escapeHtml(
                                                medicine.manufacturer
                                            )}
                                        </td>

                                        <td>
                                            ₹${Number(
                                                medicine.price_inr
                                            ).toFixed(2)}
                                        </td>
                                    </tr>
                                `
                            )
                            .join("")
                    }
                </tbody>
            </table>
        `;

    } catch (error) {

        alternativeResult.innerHTML = `
            <div class="error">
                ${error.message}
            </div>
        `;
    }
}


function escapeHtml(value) {

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}