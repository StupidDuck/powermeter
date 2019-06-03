/*
data :{
  mean,
  y_min,
  y_max,
  lables,
  values
}
*/

fetchData();

//puduku => Promise !

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

function fetchData() {
  const req = new XMLHttpRequest();

  req.onreadystatechange = function(event) {
      // XMLHttpRequest.DONE === 4
      if (this.readyState === XMLHttpRequest.DONE) {
          if (this.status === 200) {
              buildChart(JSON.parse(this.responseText));
          } else {
              console.log("Status de la réponse: %d (%s)", this.status, this.statusText);
          }
      }
  };

  req.open('GET', 'journal/chart_data', true);
  req.send(null);
}

function palette(i) {
  let colors = ["#04151f", "#183a37", "#efd6ac", "#c44900", "#432534"];
  const transparency = "FF"
  const index = i % colors.length;
  return colors[index];
}
