async function api(
    url,
    options = {}
) {

    const response = await fetch(
        url,
        {
            credentials: "same-origin",
            ...options
        }
    );

    let data = {};

    try {

        data = await response.json();

    } catch {

        data = {};

    }

    if (!response.ok) {

        throw new Error(
            data.detail ||
            "Request failed."
        );
    }

    return data;
}


async function logout() {

    try {

        await api(
            "/api/logout",
            {
                method: "POST"
            }
        );

        window.location.href = "/";

    } catch (error) {

        alert(
            error.message
        );
    }
}


function escapeHtml(value) {

    return String(value)
        .replace(
            /[&<>'"]/g,
            function (character) {

                const map = {
                    "&": "&amp;",
                    "<": "&lt;",
                    ">": "&gt;",
                    "'": "&#39;",
                    '"': "&quot;"
                };

                return map[
                    character
                ];
            }
        );
}


function showResult(
    box,
    data
) {

    box.classList.remove(
        "hidden"
    );


    const products = (
        data.products || []
    )
        .map(
            function (product) {

                return `
                    <div class="product">

                        <b>
                            ${escapeHtml(
                                product.name
                            )}
                        </b>

                        <div class="product-meta">

                            ₹${Number(
                                product.price
                            ).toLocaleString(
                                "en-IN"
                            )}

                            ·

                            ${escapeHtml(
                                product.platform
                            )}

                            ·

                            <a
                                href="${escapeHtml(
                                    product.url
                                )}"
                                target="_blank"
                                rel="noopener noreferrer"
                            >
                                Open
                            </a>

                        </div>

                    </div>
                `;
            }
        )
        .join("");


    const notes = (
        data.notes || []
    )
        .map(
            function (note) {

                return `
                    <li>
                        ${escapeHtml(note)}
                    </li>
                `;
            }
        )
        .join("");


    box.innerHTML = `

        <h3>
            ${escapeHtml(
                data.summary ||
                "Recommendation"
            )}
        </h3>


        <p>

            <b>
                Budget:
            </b>

            ₹${Number(
                data.budget || 0
            ).toLocaleString(
                "en-IN"
            )}

            &nbsp;

            <b>
                Estimated total:
            </b>

            ₹${Number(
                data.estimated_total || 0
            ).toLocaleString(
                "en-IN"
            )}

            &nbsp;

            <b>
                Remaining:
            </b>

            ₹${Number(
                data.remaining || 0
            ).toLocaleString(
                "en-IN"
            )}

        </p>


        ${
            data.image_analysis
            ?
            `
                <p>
                    ${escapeHtml(
                        data.image_analysis
                    )}
                </p>
            `
            :
            ""
        }


        <h3>
            Suggestions
        </h3>


        ${
            products ||
            "<p>No products found.</p>"
        }


        ${
            notes
            ?
            `<ul>${notes}</ul>`
            :
            ""
        }


        <small>

            Source:

            ${escapeHtml(
                data.source ||
                "unknown"
            )}

        </small>
    `;
}


async function submitJSON(
    form,
    url,
    box
) {

    try {

        const body = Object.fromEntries(
            new FormData(form).entries()
        );


        body.budget = Number(
            body.budget
        );


        if (body.guests) {

            body.guests = Number(
                body.guests
            );
        }


        const result = await api(
            url,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body:
                    JSON.stringify(body)
            }
        );


        showResult(
            box,
            result
        );

    } catch (error) {

        box.classList.remove(
            "hidden"
        );

        box.innerHTML = `
            <div class="error">
                ${escapeHtml(
                    error.message
                )}
            </div>
        `;
    }
}


async function submitForm(
    form,
    url,
    box
) {

    try {

        const result = await api(
            url,
            {
                method: "POST",
                body: new FormData(form)
            }
        );


        showResult(
            box,
            result
        );

    } catch (error) {

        box.classList.remove(
            "hidden"
        );

        box.innerHTML = `
            <div class="error">
                ${escapeHtml(
                    error.message
                )}
            </div>
        `;
    }
}


document.addEventListener(
    "DOMContentLoaded",
    function () {

        const loginForm =
            document.querySelector(
                "#loginForm"
            );


        if (loginForm) {

            loginForm.addEventListener(
                "submit",
                async function (event) {

                    event.preventDefault();

                    try {

                        await api(
                            "/api/login",
                            {
                                method: "POST",

                                headers: {
                                    "Content-Type":
                                        "application/json"
                                },

                                body:
                                    JSON.stringify(
                                        Object.fromEntries(
                                            new FormData(
                                                loginForm
                                            )
                                        )
                                    )
                            }
                        );


                        window.location.href =
                            "/dashboard";

                    } catch (error) {

                        document.querySelector(
                            "#formError"
                        ).textContent =
                            error.message;
                    }
                }
            );
        }


        const registerForm =
            document.querySelector(
                "#registerForm"
            );


        if (registerForm) {

            registerForm.addEventListener(
                "submit",
                async function (event) {

                    event.preventDefault();

                    try {

                        await api(
                            "/api/register",
                            {
                                method: "POST",

                                headers: {
                                    "Content-Type":
                                        "application/json"
                                },

                                body:
                                    JSON.stringify(
                                        Object.fromEntries(
                                            new FormData(
                                                registerForm
                                            )
                                        )
                                    )
                            }
                        );


                        window.location.href =
                            "/dashboard";

                    } catch (error) {

                        document.querySelector(
                            "#formError"
                        ).textContent =
                            error.message;
                    }
                }
            );
        }


        const homeForm =
            document.querySelector(
                "#homeForm"
            );


        if (homeForm) {

            homeForm.addEventListener(
                "submit",
                function (event) {

                    event.preventDefault();

                    submitJSON(
                        homeForm,
                        "/api/generate-home",
                        document.querySelector(
                            "#result"
                        )
                    );
                }
            );
        }


        const partyForm =
            document.querySelector(
                "#partyForm"
            );


        if (partyForm) {

            partyForm.addEventListener(
                "submit",
                function (event) {

                    event.preventDefault();

                    submitJSON(
                        partyForm,
                        "/api/generate-party",
                        document.querySelector(
                            "#result"
                        )
                    );
                }
            );
        }


        const jewelryForm =
            document.querySelector(
                "#jewelryForm"
            );


        if (jewelryForm) {

            jewelryForm.addEventListener(
                "submit",
                function (event) {

                    event.preventDefault();

                    submitForm(
                        jewelryForm,
                        "/api/generate-jewelry",
                        document.querySelector(
                            "#result"
                        )
                    );
                }
            );
        }

    }
);