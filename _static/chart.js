const leftctx = document.getElementById('leftChart').getContext('2d');
const rightctx = document.getElementById('rightChart').getContext('2d');

function setChart(ctx, rank, divisions, title_text) {
    Chart.register(ChartDataLabels);
    indexLength = divisions.length
    origin_value = divisions[indexLength - rank]
    // Sorting division, and find correct_index
    console.log(divisions.toString())
    divisions.sort((a, b) => parseInt(a) - parseInt(b))
    // console.log(divisions.toString())
    correct_index = divisions.findIndex((num) => num == origin_value)
    // label_array = divisions.map((x) => x)
    label_array = [5,4,3,2,1]
    // label_array[correct_index] = label_array[correct_index].concat(" (you)")
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
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 400,
                    title: {
                        display: true,
                        text: "報酬",
                        font: {
                            size: 14
                        }
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: "排名",
                        font: {
                            size: 14
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: title_text,
                    font: {
                        size: 14
                    }
                },
                datalabels: {
                    backgroundColor: function (context) {
                        return context.dataset.backgroundColor;
                    },
                    borderColor: function (context) {
                        return context.dataset.borderColor;
                    },
                    borderRadius: 15,
                    borderWidth: 2,
                    // color: 'white',
                    font: {
                        weight: 'bold'
                    },
                    padding: 6,
                    anchor: "end",
                    align: 'top',
                }
            }
        }
    });
}

var leftChart = setChart(leftctx, rank, origin_division, "左邊")
var rightChart = setChart(rightctx, rank, alternative_division, "右邊")
