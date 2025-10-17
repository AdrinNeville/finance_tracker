// finance/static/js/script.js

// Confirm delete action
function confirmDelete(txId) {
    if (confirm('Are you sure you want to delete this transaction?')) {
        document.getElementById('delete-form-' + txId).submit();
    }
}

// Initialize chart if data is present
document.addEventListener('DOMContentLoaded', function() {
    const chartCanvas = document.getElementById('expenseChart');
    
    if (chartCanvas && typeof Chart !== 'undefined') {
        const categories = JSON.parse(chartCanvas.dataset.categories || '[]');
        const amounts = JSON.parse(chartCanvas.dataset.amounts || '[]');
        
        if (categories.length > 0 && amounts.length > 0) {
            const ctx = chartCanvas.getContext('2d');
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: categories,
                    datasets: [{
                        label: 'Expenses by Category',
                        data: amounts,
                        backgroundColor: [
                            '#FF6384',
                            '#36A2EB',
                            '#FFCE56',
                            '#4BC0C0',
                            '#9966FF',
                            '#FF9F40',
                            '#FF6384',
                            '#C9CBCF'
                        ],
                        hoverOffset: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                        },
                        title: {
                            display: true,
                            text: 'Expenses by Category'
                        }
                    }
                }
            });
        }
    }
});

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Add smooth scroll behavior
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});