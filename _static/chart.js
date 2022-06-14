const leftctx = document.getElementById('leftChart').getContext('2d');
const rightctx = document.getElementById('rightChart').getContext('2d');

function setChart(ctx, rank, divisions, title_text) {
    label_array = divisions.map((x)=>x)
    label_array[rank - 1] = label_array[rank - 1].concat(" (you)")
    backgroundColor_array = Array(5).fill('rgba(54, 162, 235, 0.2)')
    backgroundColor_array[rank - 1] = 'rgba(255, 99, 132, 0.2)'
    borderColor_array = Array(5).fill('rgba(54, 162, 235, 1)')
    borderColor_array[rank - 1] = 'rgba(255, 99, 132, 1)'
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
                }
            }
        }
    });
}

var leftChart = setChart(leftctx, rank, origin_division, "Origin divisions")
var rightChart = setChart(rightctx, rank, alternative_division, "Alternative divisions")
