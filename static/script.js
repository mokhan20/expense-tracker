async function fetchTransactions() {
    const res = await fetch("/api/transactions");
    const data = await res.json();
    const list = document.getElementById("transaction-list");
    list.innerHTML = data.map(t =>
        `<li>${t.date} — ${t.description}: $${t.amount}</li>`
    ).join("");
}

document.getElementById("transaction-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const body = {
        amount: parseFloat(document.getElementById("amount").value),
        description: document.getElementById("description").value,
        date: document.getElementById("date").value
    };
    await fetch("/api/transactions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
    });
    fetchTransactions();
});

fetchTransactions();