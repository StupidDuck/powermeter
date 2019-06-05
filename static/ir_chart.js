var ctx = document.getElementById("myChart");

function buildChart(data) {
  var myLineChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: data.labels,
        datasets: [{
          label: 'Power Consumption',
          data: data.values,
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

function fetchData(id) {
  return new Promise((resolve, reject) => {
    const req = new XMLHttpRequest();
    req.onreadystatechange = function(event) {
        if (this.readyState === XMLHttpRequest.DONE) {
            if (this.status === 200) {
                resolve(JSON.parse(this.responseText));
            } else {
                reject("Status de la réponse: %d (%s)", this.status, this.statusText);
            }
        }
    };

    req.open('GET', '/meter/' + id + '/json', true);
    req.send(null);
  });
}

function palette(i) {
  let colors = ["#04151f", "#183a37", "#efd6ac", "#c44900", "#432534"];
  const transparency = "FF"
  const index = i % colors.length;
  return colors[index];
}
