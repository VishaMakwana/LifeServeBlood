document.addEventListener("DOMContentLoaded", function () {

    if (typeof Chart === "undefined") {
        console.error("Chart.js not loaded");
        return;
    }

    // Blood Stock Chart
    const stockCanvas = document.getElementById("stockChart");

    if (stockCanvas) {
        new Chart(stockCanvas, {
            type: "bar",
            data: {
                labels: bloodGroups,
                datasets: [{
                    label: "Available Units",
                    data: stockUnits,
                    backgroundColor: "#dc3545"
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }

    // Blood Request Status
    const statusCanvas = document.getElementById("statusChart");

    if (statusCanvas) {
        new Chart(statusCanvas, {
            type: "pie",
            data: {
                labels: ["Approved", "Pending", "Rejected"],
                datasets: [{
                    data: [
                        approvedRequests,
                        pendingRequests,
                        rejectedRequests
                    ],
                    backgroundColor: [
                        "#198754",
                        "#ffc107",
                        "#dc3545"
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }

    // Monthly Donation Chart
    const donationCanvas = document.getElementById("donationChart");

    if (donationCanvas) {
        new Chart(donationCanvas, {
            type: "line",
            data: {
                labels: months,
                datasets: [{
                    label: "Approved Donations",
                    data: donationCounts,
                    borderColor: "#198754",
                    backgroundColor: "rgba(25,135,84,0.2)",
                    fill: true,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }

    // Monthly Blood Request Chart
    const requestCanvas = document.getElementById("requestChart");

    if (requestCanvas) {
        new Chart(requestCanvas, {
            type: "line",
            data: {
                labels: requestMonths,
                datasets: [{
                    label: "Blood Requests",
                    data: requestCounts,
                    borderColor: "#dc3545",
                    backgroundColor: "rgba(220,53,69,0.2)",
                    fill: true,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }

});