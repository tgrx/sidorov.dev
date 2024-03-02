<script lang="ts">
	import { readable } from 'svelte/store';
	import me from '$lib/static/me.webp';
	import Prism from '@magidoc/plugin-svelte-prismjs';
	import ProjectsList from '$lib/ProjectsList.svelte';
	import TechStackCloud from '$lib/TechStackCloud.svelte';

	import 'prismjs/components/prism-python.js';
	import 'prismjs/components/prism-sql.js';
	import 'prismjs/plugins/normalize-whitespace/prism-normalize-whitespace.min.js';

	export let data;

	const snippet = readable(data.codeSnippet, (set) => {
		const iid = setInterval(() => {
			const idx = Math.floor(Math.random() * data.codeSnippets.length);
			set(data.codeSnippets[idx]);
		}, 8000);

		return () => {
			clearInterval(iid);
		};
	});
</script>

<svelte:head>
	<link
		rel="stylesheet"
		href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.17.1/themes/prism-okaidia.min.css"
	/>
</svelte:head>

<div class="container">
	<h1>🔥 Alexander Sidorov 🔥</h1>

	<article class="links">
		<p><a href="https://github.com/tgrx">GitHub</a></p>
		<p><a href="https://t.me/jesuisalexandre">Telegram</a></p>
		<p><a href="https://www.linkedin.com/in/alexnsidorov/">LinkedIn</a></p>
		<p><a href="https://sidorov.dev">About</a></p>
	</article>

	<article class="hero">
		<img src={me} alt="Me" class="face" />
		<section>
			<p>I am software engineer with 12+ years of experience.</p>
			<p>
				Customer experience, user experience, quality and reliability are the areas I'm focusing.
			</p>
			<p>
				Clean Architecture apologist. Full-stack wannabe. Mentor for good people. Apple fanboy.
				Father of two kids. Sailor, boxer, driver - however currently in the end of a long-term
				"vacation".
			</p>
			<p>In the meantime, backgammon player.</p>
		</section>
		<ProjectsList projects={data.projects} />
		<TechStackCloud techStack={data.techStack} />
	</article>

	<article class="ads">
		<section>
			<pre>
				<code class="code-snippet">
					<Prism language={$snippet.lang} source={$snippet.code} />
				</code>
			</pre>
		</section>
	</article>
</div>

<style>
	.container {
		padding-left: 10px;
		padding-right: 10px;
		padding-top: 10px;
	}

	.face {
		height: 300px;
		max-width: 225px;
	}

	.hero {
		align-items: stretch;
		background-repeat: no-repeat;
		display: grid;
		grid-gap: 1rem;
		grid-template-columns: repeat(auto-fit, minmax(560px, 1fr));
	}

	.ads {
		align-items: stretch;
		background-repeat: no-repeat;
		display: grid;
		grid-gap: 1rem;
		grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
	}

	.links {
		display: grid;
		grid-gap: 0.1rem;
		grid-template-columns: repeat(auto-fit, minmax(50px, 1fr));
		justify-items: center;
		align-items: stretch;
	}

	.code-snippet {
		font-family: 'Fira Code';
		font-size: 13px;
	}
</style>
