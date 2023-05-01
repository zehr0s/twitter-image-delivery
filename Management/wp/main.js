fetch('../Logs/info.log')
    .then(response => response.json())
    .then(data => {
        const dailyImagesOK = {};
        const dailyImagesError = {};
        const timestampsOK = [];
        const timestampsError = [];

        for (const timestamp in data) {
            const entry = data[timestamp];
            const dt = new Date(timestamp);
            const dateStr = dt.toISOString().split('T')[0];

            if (entry.status === 'OK') {
                dailyImagesOK[dateStr] = (dailyImagesOK[dateStr] || 0) + entry.images;
                timestampsOK.push(dt);
            } else if (entry.status === 'ERROR') {
                dailyImagesError[dateStr] = (dailyImagesError[dateStr] || 0) + entry.images;
                timestampsError.push(dt);
            }
        }

        // Sort the objects by date
        const sortedOK = Object.entries(dailyImagesOK).sort();
        const sortedError = Object.entries(dailyImagesError).sort();

        const datesOK = sortedOK.map(([date, _]) => date);
        const imagesOK = sortedOK.map(([_, images]) => images);
        const datesError = sortedError.map(([date, _]) => date);
        const imagesError = sortedError.map(([_, images]) => images);

        const createChart = (ctx, data, label, type) => {
            return new Chart(ctx, {
                type: type,
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: label,
                        data: data.data,
                        backgroundColor: data.backgroundColor,
                        borderColor: data.borderColor,
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        x: {
                            type: 'time',
                            time: {
                                unit: 'day'
                            }
                        },
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        };

        createChart(document.getElementById('images-ok').getContext('2d'), {
            labels: datesOK,
            data: imagesOK,
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)'
        }, 'Published Images per Day (Status OK)', 'bar');

        createChart(document.getElementById('images-error').getContext('2d'), {
            labels: datesError,
            data: imagesError,
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)'
        }, 'Published Images per Day (Status ERROR)', 'bar');

        createChart(document.getElementById('timestamps-ok').getContext('2d'), {
            labels: timestampsOK,
            data: new Array(timestampsOK.length).fill(1),
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)'
        }, 'Posts with Status OK by Timestamp', 'scatter');

        createChart(document.getElementById('timestamps-error').getContext('2d'), {
            labels: timestampsError,
            data: new Array(timestampsError.length).fill(1),
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)'
        }, 'Posts with Status ERROR by Timestamp', 'scatter');
    });
