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
              //unit: 'month',
              unit: 'year',
              //min: moment().subtract(6, 'month'),
            },
            ticks: {
              //min: moment().subtract(6, 'month'),
              //min: moment().subtract(4, 'year'),
              min: Math.min(...data.values.map(x => x.label)),
              max: Math.max(...data.values.map(x => x.label))
            },
            distribution: 'linear',
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
        },
        plugins: {
          zoom: {
            pan: {
              enabled: true,
              mode: 'x',
              // rangeMin: {
              //   x: 0
              // },
              // rangeMax: {
              //   x: moment()
              // }
            }
          }
        }
      },
  });

  var x = window.matchMedia("screen and (max-width:576px)").matches;
  if (x === true) {
    myLineChart.options.responsive = false;
    myLineChart.options.scales.yAxes[0].scaleLabel.display = false;
    myLineChart.options.scales.yAxes[0].gridLines.display = false;
    myLineChart.options.scales.yAxes[0].display = false;
    myLineChart.options.scales.yAxes[0].ticks.beginAtZero = true;
    //myLineChart.options.scales.xAxes[0].distribution = 'series';
  }
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

function groupByYear(journal) {
    return new Promise((resolve, reject) => {
        try {
            journal.entries = journal.entries.map((entry) => new Object({
                'year': new Date(Date.parse(entry.date)).getFullYear(),
                'id': entry.id,
                'mean_consumption_per_day': entry.mean_consumption_per_day,
                'value': entry.value,
                'duration': entry.duration
            }));

            const key = 'year';
            const reduced = journal.entries.reduce((result, item) => ({
                ...result,
                [item[key]]: [
                  ...(result[item[key]] || []),
                  item,
                ],
            }), {});

            const summed = Object.values(reduced).map((val, idx) => {
                const consumption = val.reduce((sum, index) => {
                    return sum + index.duration * index.mean_consumption_per_day
                }, 0);
                const days = val.reduce((sum, index) => {
                    return sum + index.duration
                }, 0);
                return new Object({
                    'label': `${val[0].year}-01-01`,
                    'value': (consumption / days).toFixed(2)
                });
            });

            let y_max = Math.max(...summed.map(x => x.value));
            y_max = y_max + y_max / 5;

            resolve(new Object({
                'values': summed,
                'y_min': 0,
                'y_max': y_max
            }));
        }
        catch {
            reject(console.log("Something bad happened in groupByYear..."));
        }
    });
}

function palette(i) {
  let colors = ["#04151f", "#183a37", "#efd6ac", "#c44900", "#432534"];
  const transparency = "FF"
  const index = i % colors.length;
  return colors[index];
}