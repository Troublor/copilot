import * as readline from 'readline';
import * as child_process from 'child_process';
import * as path from 'path';
import { fileURLToPath } from 'url';
import * as process from 'process';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function main() {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  const p = child_process.spawn(
    'node',
    [path.join(__dirname, '..', '..', '..', 'copilot', 'dist', 'agent.js')],
    {
      stdio: 'pipe',
    },
  );
  p.stdin.setDefaultEncoding('utf8');
  p.stdout.pipe(process.stdout);
  p.stderr.pipe(process.stderr);

  while (true) {
    await new Promise((resolve) => setTimeout(resolve, 1000));
    console.log();
    const i: string = await new Promise((resolve) =>
      rl.question('> ', (r) => resolve(r)),
    );
    try {
      const [method, param] = i.split('->');
      const obj = {
        jsonrpc: '2.0',
        id: 1,
        method,
        params: JSON.parse(param),
      };
      const content = JSON.stringify(obj);
      console.log('request: ', content);
      p.stdin.write(`Content-Length: ${content.length}` + '\r\n\r\n' + content);
    } catch (e) {
      console.error('Error: ', e);
    }
  }
}

main().catch(console.error);
