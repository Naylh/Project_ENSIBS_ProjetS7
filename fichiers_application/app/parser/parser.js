const jobs = require("node-cron");
const {PythonShell} = require('python-shell');

exports.initScheduledJobs = () => {
	const scheduledJobFunction = jobs.schedule("0 0 * * *", () => {
		console.log("Exécution du parsing automatique");
		let options = {
			args: ["-r", "-o"] 
		};
		PythonShell.run("parser/parser.py", options, function (err, result){
			if (err){
				console.log(err);
			}
			else{
				console.log(result.toString());
				console.log("Le parsing régulié a été effectué avec succès");
			}
		});
	})
	scheduledJobFunction.start();
}
