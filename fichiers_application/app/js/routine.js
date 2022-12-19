const cron = require('node-cron');

cron.schedule('*/15 * * * * *', () => {
	alert("ça marche cte merde ?");
	//forceParseDB();
})