const predictionForm = document.getElementById(
    "prediction-form"
);

const predictionResult = document.getElementById(
    "prediction-result"
);


predictionForm.addEventListener(
    "submit",
    async (event) => {
        event.preventDefault();

        predictionResult.innerHTML = "Predicting...";

        const data = {
            dosage_form:
                document.getElementById("dosage-form").value,

            pack_size:
                Number(
                    document.getElementById("pack-size").value
                ),

            pack_unit:
                document.getElementById("pack-unit").value || null,

            primary_ingredient:
                document.getElementById(
                    "primary-ingredient"
                ).value,

            primary_strength:
                document.getElementById(
                    "primary-strength"
                ).value || null,

            therapeutic_class:
                document.getElementById(
                    "therapeutic-class"
                ).value,

            num_active_ingredients:
                Number(
                    document.getElementById(
                        "num-active-ingredients"
                    ).value
                )
        };


        try {
            const response = await fetch(
                "/api/predict",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify(data)
                }
            );


            const result = await response.json();


            if (!response.ok) {
                throw new Error(
                    result.detail || "Prediction failed"
                );
            }


            predictionResult.innerHTML = `
                <div class="result">
                    Predicted Price:
                    <strong>
                        ₹${result.predicted_price.toFixed(2)}
                    </strong>
                </div>
            `;

        } catch (error) {

            predictionResult.innerHTML = `
                <div class="error">
                    ${error.message}
                </div>
            `;
        }
    }
);


const alternativeForm = document.getElementById(
    "alternative-form"
);

const alternativeResult = document.getElementById(
    "alternative-result"
);


alternativeForm.addEventListener(
    "submit",
    async (event) => {
        event.preventDefault();

        alternativeResult.innerHTML =
            "Finding alternatives...";


        const medicineName =
            document.getElementById(
                "medicine-name"
            ).value;


        try {
            const response = await fetch(
                `/api/alternatives/${encodeURIComponent(
                    medicineName
                )}`
            );


            const result = await response.json();


            if (!response.ok) {
                throw new Error(
                    result.detail || "Medicine not found"
                );
            }


            if (result.alternatives.length === 0) {
                alternativeResult.innerHTML = `
                    <div class="result">
                        No alternatives found.
                    </div>
                `;

                return;
            }


            const rows =
                result.alternatives
                    .map(
                        (medicine) => `
                            <tr>
                                <td>
                                    ${medicine.brand_name}
                                </td>

                                <td>
                                    ${medicine.manufacturer}
                                </td>

                                <td>
                                    ₹${medicine.price_inr.toFixed(2)}
                                </td>
                            </tr>
                        `
                    )
                    .join("");


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
                        ${rows}
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
);