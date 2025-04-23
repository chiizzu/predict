function updateTrendIndicator(initialPrice, prediksi) {
    console.log("updateTrendIndicator called with interval:", initialPrice, prediksi);
    const trendIndicator = document.getElementById('trendIndicator');
    if (parseFloat(initialPrice) > parseFloat(prediksi)) {
        trendIndicator.textContent = 'Bearish';
        trendIndicator.style.color = '#ff5c5c';
    } else if (parseFloat(initialPrice) < parseFloat(prediksi)) {
        trendIndicator.textContent = 'Bullish';
        trendIndicator.style.color = '#9dd99d'
    } else {
        trendIndicator.textContent = 'Neutral';
        trendIndicator.style.color = 'white'
    }
}
function perubahanHarga(initialPrice, updatedPrice){
    const priceChange = initialPrice - updatedPrice;
    const change = document.getElementsByClassName('change');
}

const currentHarga = initialPriceFromTemplate;
const predictedHarga = predictedPriceFromTemplate;
const updatedHarga = updatedPriceFromTemplate;

updateTrendIndicator(currentHarga, predictedHarga);

/*
setInterval( () => {
    location.reload()
}, 2000)

*/