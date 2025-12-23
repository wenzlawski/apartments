import type { SpawnOptionsWithoutStdio } from 'child_process';
import { spawn } from 'child_process';

const spawnOptions: SpawnOptionsWithoutStdio = {
	stdio: 'inherit'
};

const run = async () => {
	spawn('npm', ['run', 'format'], spawnOptions);
	spawn('npm', ['run', 'lint'], spawnOptions);

	// process.on('SIGINT', async () => {
	// 	console.log('Cleaning up...');
	// 	// spawn('npm', ['run', 'db:down'], spawnOptions);
	// });
};

run();
