// script.js - Client-side JavaScript for Deep6 Trading Platform

document.addEventListener('DOMContentLoaded', () => {
    const apiUrl = 'http://localhost:5000/api';
    const tradeForm = document.getElementById('trade-form');
    const tradeHistorySection = document.getElementById('trade-history');
    const balanceDisplay = document.getElementById('balance');

    // Fetch and display user balance
    const fetchBalance = async () => {
        try {
            const response = await fetch(`${apiUrl}/balance`);
            const data = await response.json();
            balanceDisplay.textContent = `$${data.balance.toFixed(2)}`;
        } catch (error) {
            console.error('Error fetching balance:', error);
            balanceDisplay.textContent = 'Error loading balance';
        }
    };

    // Fetch and display trade history
    const fetchTradeHistory = async () => {
        try {
            const response = await fetch(`${apiUrl}/trades`);
            const trades = await response.json();
            tradeHistorySection.innerHTML = trades.map(trade => `
                <div class="trade-item">
                    <p><strong>Symbol:</strong> ${trade.symbol}</p>
                    <p><strong>Type:</strong> ${trade.type}</p>
                    <p><strong>Quantity:</strong> ${trade.quantity}</p>
                    <p><strong>Price:</strong> $${trade.price.toFixed(2)}</p>
                    <p><strong>Date:</strong> ${new Date(trade.date).toLocaleString()}</p>
                </div>
            `).join('');
        } catch (error) {
            console.error('Error fetching trade history:', error);
            tradeHistorySection.innerHTML = '<p>Error loading trade history</p>';
        }
    };

    // Handle trade form submission
    tradeForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(tradeForm);
        const symbol = formData.get('symbol');
        const type = formData.get('type');
        const quantity = formData.get('quantity');

        try {
            const response = await fetch(`${apiUrl}/trade`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ symbol, type, quantity })
            });

            if (response.ok) {
                alert('Trade executed successfully!');
                fetchBalance();
                fetchTradeHistory();
                tradeForm.reset();
            } else {
                const errorData = await response.json();
                alert(`Error: ${errorData.error}`);
            }
        } catch (error) {
            console.error('Error executing trade:', error);
            alert('Failed to execute trade. Please try again.');
        }
    });

    // Initial data fetch
    fetchBalance();
    fetchTradeHistory();
});