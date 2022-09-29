const ctx = document.getElementById('result').getContext('2d');

function setChart(ctx, rank, divisions, title_text) {
    Chart.register(ChartDataLabels);
    indexLength = divisions.length
    correct_index = indexLength - rank
    label_array = divisions.map((x) => x)
    label_array[correct_index] = label_array[correct_index].concat(" (you)")
    backgroundColor_array = Array(5).fill('rgba(54, 162, 235, 0.2)')
    backgroundColor_array[correct_index] = 'rgba(255, 99, 132, 0.2)'
    borderColor_array = Array(5).fill('rgba(54, 162, 235, 1)')
    borderColor_array[correct_index] = 'rgba(255, 99, 132, 1)'
    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: label_array,
            datasets: [{
                data: divisions,
                backgroundColor: backgroundColor_array,
                borderColor: borderColor_array,
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: title_text
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                datalabels: {
                    backgroundColor: function (context) {
                        return context.dataset.backgroundColor;
                    },
                    borderColor: function (context) {
                        return context.dataset.borderColor;
                    },
                    borderRadius: 25,
                    borderWidth: 2,
                    // color: 'white',
                    font: {
                        weight: 'bold'
                    },
                    padding: 4,
                }
            }
        }
    });
}

var chart = setChart(ctx, rank, division, "divisions")
