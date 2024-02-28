const codePy = `
def decorator(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        t0 = time.monotonic()
        try:
            return func(*args, **kwargs)
        finally:
            dt = time.monotonic() - t0
            print(f"{func.__name__} took {dt:.3f} seconds")
    return decorated
`;

const codeJs = `
    const syncInterval = setInterval(async () => {
        const response = await fetch(url, {method: 'POST'});
        response.json().then((obj) => {
            console.log("Obj: " + JSON.stringify(obj));
        });
    });
`;

const codeSql = `
    WITH ranked AS (
        SELECT book_id, rank() OVER (
            PARTITION BY book_id
            ORDER BY author_id) AS some_rank
        -- will fix it later, you know
    )
    SELECT * FROM ranked JOIN some_table ON random() < 0.5;
`;

const codeSnippets = [codeJs, codeSql, codePy];

const technologies = [
	'API dvelopment',
	'Chat bots',
	'Clean Architecture',
	'Django',
	'Docker and Compose',
	'FastAPI',
	'Fully-automated E2E tests',
	'Gentoo Linux',
	'Github Actions',
	'Good unit-testing howto',
	'JSON in RDBMS',
	'Linux',
	'Mac OS X',
	'Mentoring',
	'MongoDB',
	'PostgreSQL',
	'Project planning',
	'Python',
	'Redis',
	'Software architecture',
	'SRP',
	'Svelte',
	'SvelteKit',
	'Telegram bots'
].sort(() => {
	return Math.sign(0.5 - Math.random());
});

export function load() {
	const idx = Math.floor(Math.random() * codeSnippets.length);
	const codeSnippet = codeSnippets[idx];

	return {
		codeSnippet,
		codeSnippets,
		technologies
	};
}
