/**
 * StockSense AI - Plotly.js Financial Charting Engine
 * Creates institutional-grade candlestick charts, volume subplots, indicator overlays,
 * portfolio allocation donuts, and comparative line charts.
 */

const CHART_THEME = {
  paper_bgcolor: '#161b22',
  plot_bgcolor: '#161b22',
  font: {
    family: 'Inter, -apple-system, sans-serif',
    color: '#8b949e',
    size: 11
  },
  gridcolor: '#21262d',
  color_up: '#2ea043',
  color_down: '#f85149',
};

class StockSenseCharts {

  /**
   * Render Candlestick or Line Chart with Volume Subplot and Technical Indicators.
   */
  static renderStockChart(containerId, candleData, indicatorsData = null, chartType = 'candlestick', activeOverlays = []) {
    const container = document.getElementById(containerId);
    if (!container || !candleData || candleData.length === 0) return;

    const dates = candleData.map(c => c.date);
    const opens = candleData.map(c => c.open);
    const highs = candleData.map(c => c.high);
    const lows = candleData.map(c => c.low);
    const closes = candleData.map(c => c.close);
    const volumes = candleData.map(c => c.volume);

    const traces = [];

    // 1. Primary Price Trace
    if (chartType === 'candlestick') {
      traces.push({
        x: dates,
        open: opens,
        high: highs,
        low: lows,
        close: closes,
        type: 'candlestick',
        name: 'Price (OHLC)',
        increasing: { line: { color: CHART_THEME.color_up, width: 1.5 }, fillcolor: CHART_THEME.color_up },
        decreasing: { line: { color: CHART_THEME.color_down, width: 1.5 }, fillcolor: CHART_THEME.color_down },
        yaxis: 'y'
      });
    } else {
      traces.push({
        x: dates,
        y: closes,
        type: 'scatter',
        mode: 'lines',
        name: 'Close Price',
        line: { color: '#58a6ff', width: 2 },
        yaxis: 'y'
      });
    }

    // 2. Technical Indicator Overlays
    if (indicatorsData && indicatorsData.series) {
      const s = indicatorsData.series;

      if (activeOverlays.includes('sma_20') && s.sma_20) {
        traces.push({
          x: dates, y: s.sma_20,
          type: 'scatter', mode: 'lines',
          name: 'SMA 20', line: { color: '#f0883e', width: 1.5 },
          yaxis: 'y'
        });
      }
      if (activeOverlays.includes('sma_50') && s.sma_50) {
        traces.push({
          x: dates, y: s.sma_50,
          type: 'scatter', mode: 'lines',
          name: 'SMA 50', line: { color: '#bc8cff', width: 1.5 },
          yaxis: 'y'
        });
      }
      if (activeOverlays.includes('sma_200') && s.sma_200) {
        traces.push({
          x: dates, y: s.sma_200,
          type: 'scatter', mode: 'lines',
          name: 'SMA 200', line: { color: '#3fb950', width: 1.5 },
          yaxis: 'y'
        });
      }
      if (activeOverlays.includes('ema_12') && s.ema_12) {
        traces.push({
          x: dates, y: s.ema_12,
          type: 'scatter', mode: 'lines',
          name: 'EMA 12', line: { color: '#38bdf8', width: 1.5 },
          yaxis: 'y'
        });
      }
      if (activeOverlays.includes('bollinger') && s.bb_upper && s.bb_lower) {
        traces.push({
          x: dates, y: s.bb_upper,
          type: 'scatter', mode: 'lines',
          name: 'BB Upper (2σ)', line: { color: '#79c0ff', width: 1, dash: 'dot' },
          yaxis: 'y'
        });
        traces.push({
          x: dates, y: s.bb_lower,
          type: 'scatter', mode: 'lines',
          name: 'BB Lower (2σ)', line: { color: '#79c0ff', width: 1, dash: 'dot' },
          fill: 'tonexty', fillcolor: 'rgba(56, 189, 248, 0.05)',
          yaxis: 'y'
        });
      }
    }

    // 3. Volume Bar Subplot
    const volColors = closes.map((c, i) => {
      if (i === 0) return 'rgba(139, 148, 158, 0.5)';
      return c >= closes[i - 1] ? 'rgba(46, 160, 67, 0.4)' : 'rgba(248, 81, 73, 0.4)';
    });

    traces.push({
      x: dates,
      y: volumes,
      type: 'bar',
      name: 'Volume',
      marker: { color: volColors },
      yaxis: 'y2'
    });

    const layout = {
      dragmode: 'zoom',
      showlegend: true,
      legend: {
        orientation: 'h',
        x: 0, y: 1.08,
        font: { color: '#c9d1d9', size: 10 }
      },
      margin: { l: 45, r: 25, t: 30, b: 30 },
      paper_bgcolor: CHART_THEME.paper_bgcolor,
      plot_bgcolor: CHART_THEME.plot_bgcolor,
      xaxis: {
        rangeslider: { visible: false },
        gridcolor: CHART_THEME.gridcolor,
        color: '#8b949e',
        tickformat: '%b %d',
      },
      yaxis: {
        domain: [0.25, 1],
        gridcolor: CHART_THEME.gridcolor,
        color: '#8b949e',
        autorange: true
      },
      yaxis2: {
        domain: [0, 0.20],
        gridcolor: CHART_THEME.gridcolor,
        color: '#6e7681',
        showticklabels: false
      }
    };

    const config = {
      responsive: true,
      displayModeBar: true,
      displaylogo: false,
      modeBarButtonsToRemove: ['lasso2d', 'select2d']
    };

    Plotly.newPlot(containerId, traces, layout, config);
  }

  /**
   * Render RSI Subplot.
   */
  static renderRSIChart(containerId, dates, rsiValues) {
    const container = document.getElementById(containerId);
    if (!container || !dates || !rsiValues) return;

    const trace = {
      x: dates, y: rsiValues,
      type: 'scatter', mode: 'lines',
      name: 'RSI (14)',
      line: { color: '#bc8cff', width: 2 }
    };

    const layout = {
      margin: { l: 45, r: 25, t: 15, b: 25 },
      paper_bgcolor: CHART_THEME.paper_bgcolor,
      plot_bgcolor: CHART_THEME.plot_bgcolor,
      font: CHART_THEME.font,
      xaxis: { gridcolor: CHART_THEME.gridcolor, color: '#8b949e' },
      yaxis: {
        gridcolor: CHART_THEME.gridcolor, color: '#8b949e',
        range: [0, 100],
        tickvals: [30, 50, 70]
      },
      shapes: [
        { type: 'line', x0: dates[0], x1: dates[dates.length - 1], y0: 70, y1: 70, line: { color: 'rgba(248, 81, 73, 0.6)', dash: 'dot', width: 1 } },
        { type: 'line', x0: dates[0], x1: dates[dates.length - 1], y0: 30, y1: 30, line: { color: 'rgba(46, 160, 67, 0.6)', dash: 'dot', width: 1 } }
      ]
    };

    Plotly.newPlot(containerId, [trace], layout, { responsive: true, displayModeBar: false });
  }

  /**
   * Render Asset Allocation Donut Chart.
   */
  static renderAllocationChart(containerId, labels, values) {
    const container = document.getElementById(containerId);
    if (!container || !labels || labels.length === 0) return;

    const trace = {
      labels: labels,
      values: values,
      type: 'pie',
      hole: 0.6,
      textinfo: 'label+percent',
      textposition: 'outside',
      automargin: true,
      marker: {
        colors: ['#58a6ff', '#2ea043', '#bc8cff', '#f0883e', '#e3b341', '#38bdf8', '#f85149', '#79c0ff']
      }
    };

    const layout = {
      margin: { l: 15, r: 15, t: 15, b: 15 },
      paper_bgcolor: 'transparent',
      font: CHART_THEME.font,
      showlegend: false
    };

    Plotly.newPlot(containerId, [trace], layout, { responsive: true, displayModeBar: false });
  }

  /**
   * Render Test Evaluation vs Forecast Line Chart.
   */
  static renderForecastChart(containerId, actualDates, actualPrices, predPrices, futurePrices) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const traces = [];

    // 1. Actual Test Historical Prices
    if (actualPrices && actualPrices.length > 0) {
      traces.push({
        x: actualDates,
        y: actualPrices,
        type: 'scatter',
        mode: 'lines',
        name: 'Actual Price',
        line: { color: '#f0f6fc', width: 2 }
      });
    }

    // 2. Test Out-of-sample Model Predictions
    if (predPrices && predPrices.length > 0) {
      traces.push({
        x: actualDates,
        y: predPrices,
        type: 'scatter',
        mode: 'lines',
        name: 'Test Prediction (Validation)',
        line: { color: '#bc8cff', width: 1.5, dash: 'dot' }
      });
    }

    // 3. Multi-day Future Forecast
    if (futurePrices && futurePrices.length > 0) {
      const futureDates = [];
      const lastDate = actualDates && actualDates.length > 0 ? new Date(actualDates[actualDates.length - 1]) : new Date();
      for (let i = 1; i <= futurePrices.length; i++) {
        const d = new Date(lastDate);
        d.setDate(d.getDate() + i);
        futureDates.push(d.toISOString().split('T')[0]);
      }

      traces.push({
        x: futureDates,
        y: futurePrices,
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Future Forecast (Projection)',
        line: { color: '#58a6ff', width: 2.5 },
        marker: { size: 5, color: '#58a6ff' }
      });
    }

    const layout = {
      margin: { l: 45, r: 25, t: 25, b: 35 },
      paper_bgcolor: CHART_THEME.paper_bgcolor,
      plot_bgcolor: CHART_THEME.plot_bgcolor,
      font: CHART_THEME.font,
      showlegend: true,
      legend: { orientation: 'h', x: 0, y: 1.12, font: { color: '#c9d1d9', size: 10 } },
      xaxis: { gridcolor: CHART_THEME.gridcolor, color: '#8b949e' },
      yaxis: { gridcolor: CHART_THEME.gridcolor, color: '#8b949e', autorange: true }
    };

    Plotly.newPlot(containerId, traces, layout, { responsive: true, displayModeBar: false });
  }
}

window.StockSenseCharts = StockSenseCharts;
