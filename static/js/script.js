document.addEventListener('DOMContentLoaded', function () {
    function formatCurrency(amount) {
        return parseFloat(amount).toFixed(2) + ' RON';
    }

    function formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('ro-RO');
    }


});