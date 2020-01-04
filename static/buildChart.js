function buildChart(ctx, data) {
  var myLineChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: data.values.map(x => x.label),
        datasets: [{
          label: 'Power Consumption',
          data: data.values.map(x => x.value),
          backgroundColor: data.values.map((val, i) => palette(i))
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        legend: {
            display: false,
        },
        scales: {
          xAxes: [{
            type: 'time',
            time: {
              unit: 'month'
            },
            distribution: 'linear',
            barThickness: 'flex',
            barPercentage: 0.9,
            categoryPercentage: 1.0
          }],
          yAxes: [{
            ticks: {
              beginAtZero: false,
              min: data.y_min,
              max: data.y_max
            },
            scaleLabel: {
              display: true,
              labelString: 'KWh / day'
            }
          }]
        }
      },
  });
}

function palette(i) {
  let colors = ["#04151f", "#183a37", "#efd6ac", "#c44900", "#432534"];
  const transparency = "FF"
  const index = i % colors.length;
  return colors[index];
}