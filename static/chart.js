function buildChart(ctx, data) {
  var myLineChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: data.values.map(x => x.label),
        datasets: [{
          label: 'Power Consumption',
          data: data.values.map(x => x.value),
          backgroundColor: data.values.map((val, i) => palette(i)),
          barPercentage: 0.9,
          categoryPercentage: 1.0,
          barThickness: 'flex'
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
            //barThickness: 'flex',
            //barPercentage: 0.9,
            //categoryPercentage: 1.0
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

function formatForChart(journal) {
  return new Promise((resolve, reject) => {
    try {
      let chart_data = {
        'y_min': 0.0,
        'y_max': 0.0,
        'values': []
      };

      journal.entries.slice(1).map(entry => {
        chart_data.values.push({'label': entry.date, 'value': entry.mean_consumption_per_day}); 
      });
      
      const chart_max = Math.max(...chart_data.values.map(x => x.value));
      const chart_min = Math.min(...chart_data.values.map(x => x.value));
      chart_data.y_max = chart_max + chart_max / 5;
      chart_data.y_min = chart_min + chart_min / 5;

      resolve({
        'values': chart_data.values,
        'mean': journal.mean,
        'y_min': chart_data.y_min,
        'y_max': chart_data.y_max,
      });
    }
    catch {
      reject(console.log("Something bad happened..."));
    }
  });
}

function palette(i) {
  let colors = ["#04151f", "#183a37", "#efd6ac", "#c44900", "#432534"];
  const transparency = "FF"
  const index = i % colors.length;
  return colors[index];
}