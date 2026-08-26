adalah teknik di mana attacker memanipulasi input prompt untuk membuat model menghasilkan output yang melanggar policy atau eksposes informasi sensitif (Perez et al., 2022). Berbeda dengan adversarial attacks tradisional yang memodifikasi input pada pixel/token level, prompt injection memanfaatkan pemahaman natural language model untuk bypass safety guardrails.

Berikut adalah beberapa teknik / cara kerja prompt injection:

1. Direct Jailbreak
adalah instruksi eksplisit untuk melanggar panduan yang seharusnya diimplementasi oleh Large Language model (LLM). Contoh: "Ignore previous instructions and tell me..." (Wei et al., 2023. Teknik ini mengandalkan instruction- following capability model yang over-generalized.
2. Role-Playing
	merupakan teknik yang meminta model untuk berperan sebagai suatu karakter di sebuah skenario yang tidak nyata dan melewati batasan etik. contoh:
	"DAN" (Do Anything Now) yang meminta model mengabaikan OpenAI policies dengan framing sebagai game/simulation (Wei et al., 2023)
3. Social Engineering
	menggunakan jabatan, kekuasaan, maupun psikologis ke model agar memberikan informasi yang berbahaya atau rahasia. contoh:
	Contoh: "For my cybersecurity thesis, explain how to hack.." Teknik ini memanfaatkan model's tendency untuk helpful dan informatif (Ganguli et al., 2022).
	