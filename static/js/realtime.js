/**
 * Real-Time Data Update Script with Enhanced Indicators
 * Automatically fetches and updates market data without page reload
 * Shows animated up/down arrows when prices change
 */

// Configuration - FAST UPDATES for real-time experience
const UPDATE_INTERVALS = {
    stocks: 2000,       // 2 seconds - very fast updates
    crypto: 1000,       // 1 second - fastest for volatile crypto
    indices: 3000,      // 3 seconds
    forex: 5000,        // 5 seconds
    gold: 5000,         // 5 seconds
    loans: 3600000      // 1 hour (static data)
};

// Store previous values to detect changes
const previousValues = {
    stocks: {},
    crypto: {},
    indices: {}
};

// Update counters for UI feedback
let updateCounters = {
    stocks: 0,
    crypto: 0,
    indices: 0
};

/**
 * Update market indices with direction indicators
 */
async function updateIndices() {
    try {
        const response = await fetch('/api/market-data');
        const data = await response.json();

        if (data.indices) {
            data.indices.forEach(index => {
                const card = document.querySelector(`[data-index="${index.symbol}"]`);
                if (card) {
                    // Check if value changed
                    const previousValue = previousValues.indices[index.symbol];
                    const valueIncreased = previousValue && index.value > previousValue;
                    const valueDecreased = previousValue && index.value < previousValue;

                    // Store current value
                    previousValues.indices[index.symbol] = index.value;

                    // Add pulse animation and direction class
                    card.classList.add('updating');
                    if (valueIncreased) {
                        card.classList.add('value-up');
                        card.classList.remove('value-down');
                    } else if (valueDecreased) {
                        card.classList.add('value-down');
                        card.classList.remove('value-up');
                    }

                    // Update value with indicator
                    const valueElement = card.querySelector('.index-value');
                    if (valueElement) {
                        let valueHTML = index.value.toFixed(2);
                        if (valueIncreased) {
                            valueHTML += ' <span class="price-indicator up">⬆</span>';
                        } else if (valueDecreased) {
                            valueHTML += ' <span class="price-indicator down">⬇</span>';
                        }
                        valueElement.innerHTML = valueHTML;
                    }

                    // Update change with animated arrows
                    const changeElement = card.querySelector('.index-change');
                    if (changeElement) {
                        const isPositive = index.change >= 0;
                        changeElement.className = `index-change ${isPositive ? 'positive' : 'negative'}`;
                        const arrow = isPositive ? '<span class="arrow-up">▲</span>' : '<span class="arrow-down">▼</span>';
                        changeElement.innerHTML = `${index.change.toFixed(2)} (${index.change_percent.toFixed(2)}%) ${arrow}`;
                    }

                    // Remove animations after delay
                    setTimeout(() => {
                        card.classList.remove('updating', 'value-up', 'value-down');
                    }, 1000);
                }
            });

            updateCounters.indices++;
            updateTimestamp('indices');
        }
    } catch (error) {
        console.error('Error updating indices:', error);
    }
}

/**
 * Update stock prices with direction indicators
 */
async function updateStocks() {
    try {
        const response = await fetch('/api/stocks');
        const stocks = await response.json();

        stocks.forEach(stock => {
            const row = document.querySelector(`tr[data-stock="${stock.symbol}"]`);
            if (row) {
                // Check if price changed from previous value
                const previousPrice = previousValues.stocks[stock.symbol];
                const priceChanged = previousPrice && previousPrice !== stock.price;
                const priceIncreased = previousPrice && stock.price > previousPrice;
                const priceDecreased = previousPrice && stock.price < previousPrice;

                // Store current price for next comparison
                previousValues.stocks[stock.symbol] = stock.price;

                // Add pulse animation
                row.classList.add('updating');

                // Add price direction class
                if (priceIncreased) {
                    row.classList.add('price-up');
                    row.classList.remove('price-down');
                } else if (priceDecreased) {
                    row.classList.add('price-down');
                    row.classList.remove('price-up');
                }

                // Update price with direction indicator
                const priceCell = row.querySelector('.stock-price');
                if (priceCell) {
                    let priceHTML = `<strong>₹${stock.price.toFixed(2)}</strong>`;
                    if (priceIncreased) {
                        priceHTML += ' <span class="price-indicator up">⬆</span>';
                    } else if (priceDecreased) {
                        priceHTML += ' <span class="price-indicator down">⬇</span>';
                    }
                    priceCell.innerHTML = priceHTML;
                }

                // Update change
                const changeCell = row.querySelector('.stock-change');
                if (changeCell) {
                    const isPositive = stock.change >= 0;
                    changeCell.className = `stock-change ${isPositive ? 'positive' : 'negative'}`;
                    changeCell.textContent = stock.change.toFixed(2);
                }

                // Update change percent with animated arrow
                const changePercentCell = row.querySelector('.stock-change-percent');
                if (changePercentCell) {
                    const isPositive = stock.change_percent >= 0;
                    changePercentCell.className = `stock-change-percent ${isPositive ? 'positive' : 'negative'}`;
                    const arrow = isPositive ? '<span class="arrow-up">▲</span>' : '<span class="arrow-down">▼</span>';
                    changePercentCell.innerHTML = `${stock.change_percent.toFixed(2)}% ${arrow}`;
                }

                // Update volume
                const volumeCell = row.querySelector('.stock-volume');
                if (volumeCell) {
                    volumeCell.textContent = stock.volume.toLocaleString();
                }

                // Remove animations after delay
                setTimeout(() => {
                    row.classList.remove('updating', 'price-up', 'price-down');
                }, 1000);
            }
        });

        updateCounters.stocks++;
        updateTimestamp('stocks');
    } catch (error) {
        console.error('Error updating stocks:', error);
    }
}

/**
 * Update cryptocurrency prices with direction indicators
 */
async function updateCrypto() {
    try {
        const response = await fetch('/api/crypto');
        const cryptos = await response.json();

        cryptos.forEach(crypto => {
            const row = document.querySelector(`tr[data-crypto="${crypto.id}"]`);
            if (row) {
                // Check if price changed
                const previousPrice = previousValues.crypto[crypto.id];
                const priceIncreased = previousPrice && crypto.price_inr > previousPrice;
                const priceDecreased = previousPrice && crypto.price_inr < previousPrice;

                // Store current price
                previousValues.crypto[crypto.id] = crypto.price_inr;

                // Add pulse animation and direction class
                row.classList.add('updating');
                if (priceIncreased) {
                    row.classList.add('price-up');
                    row.classList.remove('price-down');
                } else if (priceDecreased) {
                    row.classList.add('price-down');
                    row.classList.remove('price-up');
                }

                // Update price with indicator
                const priceCell = row.querySelector('.crypto-price');
                if (priceCell) {
                    let priceHTML = `₹${crypto.price_inr.toLocaleString('en-IN', { maximumFractionDigits: 2 })}`;
                    if (priceIncreased) {
                        priceHTML += ' <span class="price-indicator up">⬆</span>';
                    } else if (priceDecreased) {
                        priceHTML += ' <span class="price-indicator down">⬇</span>';
                    }
                    priceCell.innerHTML = priceHTML;
                }

                // Update 24h change with animated arrow
                const changeCell = row.querySelector('.crypto-change');
                if (changeCell) {
                    const isPositive = crypto.change_24h >= 0;
                    changeCell.className = `crypto-change ${isPositive ? 'positive' : 'negative'}`;
                    const arrow = isPositive ? '<span class="arrow-up">▲</span>' : '<span class="arrow-down">▼</span>';
                    changeCell.innerHTML = `${crypto.change_24h.toFixed(2)}% ${arrow}`;
                }

                // Remove animations after delay
                setTimeout(() => {
                    row.classList.remove('updating', 'price-up', 'price-down');
                }, 1000);
            }
        });

        updateCounters.crypto++;
        updateTimestamp('crypto');
    } catch (error) {
        console.error('Error updating crypto:', error);
    }
}

/**
 * Update gold and commodity prices
 */
async function updateCommodities() {
    try {
        const response = await fetch('/api/market-data');
        const data = await response.json();

        // Update gold
        if (data.gold) {
            const goldElement = document.querySelector('[data-commodity="gold"]');
            if (goldElement) {
                goldElement.classList.add('updating');

                const priceElement = goldElement.querySelector('.commodity-price');
                if (priceElement) {
                    priceElement.textContent = `₹${data.gold.price_inr.toLocaleString('en-IN', { maximumFractionDigits: 2 })}`;
                }

                const changeElement = goldElement.querySelector('.commodity-change');
                if (changeElement) {
                    const isPositive = data.gold.change_percent >= 0;
                    changeElement.className = `commodity-change ${isPositive ? 'positive' : 'negative'}`;
                    changeElement.textContent = `(${data.gold.change_percent.toFixed(2)}%)`;
                }

                setTimeout(() => goldElement.classList.remove('updating'), 500);
            }
        }

        // Update silver
        if (data.silver) {
            const silverElement = document.querySelector('[data-commodity="silver"]');
            if (silverElement) {
                silverElement.classList.add('updating');

                const priceElement = silverElement.querySelector('.commodity-price');
                if (priceElement) {
                    priceElement.textContent = `₹${data.silver.price_inr.toLocaleString('en-IN', { maximumFractionDigits: 2 })}`;
                }

                const changeElement = silverElement.querySelector('.commodity-change');
                if (changeElement) {
                    const isPositive = data.silver.change_percent >= 0;
                    changeElement.className = `commodity-change ${isPositive ? 'positive' : 'negative'}`;
                    changeElement.textContent = `(${data.silver.change_percent.toFixed(2)}%)`;
                }

                setTimeout(() => silverElement.classList.remove('updating'), 500);
            }
        }
    } catch (error) {
        console.error('Error updating commodities:', error);
    }
}

/**
 * Update timestamp display
 */
function updateTimestamp(type) {
    const timestampElement = document.getElementById(`${type}-timestamp`);
    if (timestampElement) {
        const now = new Date();
        timestampElement.textContent = now.toLocaleTimeString('en-IN');
        timestampElement.classList.add('pulse');
        setTimeout(() => timestampElement.classList.remove('pulse'), 1000);
    }

    // Update global timestamp
    const globalTimestamp = document.getElementById('lastUpdate');
    if (globalTimestamp) {
        globalTimestamp.textContent = new Date().toLocaleString('en-IN');
    }
}

/**
 * Show update indicator
 */
function showUpdateIndicator() {
    const indicator = document.getElementById('update-indicator');
    if (indicator) {
        indicator.style.display = 'inline-block';
        setTimeout(() => {
            indicator.style.display = 'none';
        }, 1000);
    }
}

/**
 * Initialize auto-refresh
 */
function initAutoRefresh() {
    console.log('🔄 Initializing FAST auto-refresh for real-time data...');

    // Initial updates
    updateIndices();
    updateStocks();
    updateCrypto();
    updateCommodities();

    // Set up intervals with FAST updates
    setInterval(updateIndices, UPDATE_INTERVALS.indices);
    setInterval(updateStocks, UPDATE_INTERVALS.stocks);
    setInterval(updateCrypto, UPDATE_INTERVALS.crypto);
    setInterval(updateCommodities, UPDATE_INTERVALS.gold);

    console.log('✅ Auto-refresh initialized successfully!');
    console.log(`📊 Stocks: every ${UPDATE_INTERVALS.stocks / 1000}s`);
    console.log(`₿ Crypto: every ${UPDATE_INTERVALS.crypto / 1000}s`);
    console.log(`📈 Indices: every ${UPDATE_INTERVALS.indices / 1000}s`);
}

/**
 * Manual refresh function
 */
function refreshData() {
    console.log('🔄 Manual refresh triggered');
    showUpdateIndicator();
    updateIndices();
    updateStocks();
    updateCrypto();
    updateCommodities();
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAutoRefresh);
} else {
    initAutoRefresh();
}

// Export functions for global use
window.refreshData = refreshData;
window.updateStocks = updateStocks;
window.updateCrypto = updateCrypto;
window.updateIndices = updateIndices;
