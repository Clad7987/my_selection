let allData = {}; // Variável global para armazenar dados do JSON

// Função para carregar JSON com imagens e vídeos
function loadImages() {
	fetch("data/data.json") // Caminho para o arquivo JSON
		.then((response) => response.json()) // Converter resposta para JSON
		.then((data) => {
			allData = data; // Armazena os dados no escopo global
			createTabs(data); // Cria abas com base nas chaves do JSON
			loadGallery("tumblr"); // Carrega todas as imagens inicialmente
			adjustImages();
		})
		.catch((error) =>
			console.error("Error loading images and videos:", error)
		);
}

// Função para criar abas
function createTabs(data) {
	const tabsList = document.querySelector("#tabs ul");
	tabsList.innerHTML = ""; // Limpa abas existentes

	const allLength = allData.tumblr.images.length + allData.tumblr.videos.length + allData.reddit.images.length + allData.reddit.videos.length + allData.unknow.images.length + allData.unknow.videos.length + allData.special.images.length + allData.special.images.length

	const allTab = document.createElement("li");
	allTab.classList.add("is-active");
	allTab.innerHTML = `<a class="text-white" onclick="loadGallery('all')">All ${allLength}</a>`;
	allTab.setAttribute("id", "all");
	tabsList.appendChild(allTab);

	for (const category in data) {
		if (data.hasOwnProperty(category)) {
			const tab = document.createElement("li");
			tab.setAttribute("id", category);
			tab.innerHTML = `<a class="text-white" onclick="loadGallery('${category}')">${
				category.charAt(0).toUpperCase() + category.slice(1)
			} (${(
				data[category].images.length + data[category].videos.length
			)})</a>`;
			tabsList.appendChild(tab);
		}
	}
}

// Função para carregar imagens de uma categoria específica
function loadGallery(category) {
	const gallery = document.getElementById("gallery");
	gallery.innerHTML = ""; // Limpa a galeria

	document.getElementById(category).classList.add("is-active");
	document
		.querySelectorAll(".is-active")
		.forEach((item) =>
			item.id !== category ? item.classList.remove("is-active") : ""
		);

	if (category === "all") {
		for (const cat in allData) {
			if (allData.hasOwnProperty(cat)) {
				loadCategoryImages(allData[cat], gallery);
			}
		}
	} else if (allData[category]) {
		loadCategoryImages(allData[category], gallery);
	}
}

function adjustImages(image) {
	const gallery = document.getElementById("gallery");
	if (document.querySelector(".is-active").innerHTML.includes("Special")) {
		gallery.style.columnCount = 1;
		document.querySelectorAll('iframe').forEach(item => {
			item.removeAttribute('width')
			item.removeAttribute('height')
			item.style.width = '100%'
			item.style.aspectRatio = '1'
			item.parentElement.style.scrollSnapAlign= 'start'
		})
		gallery.style.scrollSnapType = 'y mandatory'

	} else {
		gallery.style.columnCount = 3
		const width = image.width;
		const height = image.height;
		if (width > height) {
			image.classList.add("full");
			image.parentElement.classList.add("full");
		}
	}
}

async function loadCategoryImages(data, gallery) {
	// Função auxiliar para carregar e juntar arquivos binários
	async function fetchAndCombineParts(urls) {
		const responses = await Promise.all(
			urls.map((url) => fetch(url).then((res) => res.arrayBuffer()))
		);
		const totalLength = responses.reduce(
			(sum, buffer) => sum + buffer.byteLength,
			0
		);
		const combinedBuffer = new Uint8Array(totalLength);

		let offset = 0;
		responses.forEach((buffer) => {
			combinedBuffer.set(new Uint8Array(buffer), offset);
			offset += buffer.byteLength;
		});

		return new Blob([combinedBuffer]);
	}

	// Processar imagens
	data.images.forEach(async (item) => {
		let blobUrl;
		if (Array.isArray(item.path)) {
			// Se item.path for uma lista, carregar e juntar os arquivos
			const combinedBlob = await fetchAndCombineParts(item.path);
			blobUrl = URL.createObjectURL(combinedBlob);
			console.log(`${item.path}: ${blobUrl}`)
		} else if (typeof item.path === "string") {
			// Se item.path for uma string, usar diretamente
			blobUrl = item.path;
		}

		if (blobUrl && !blobUrl.includes("iframe")) {
			const link = document.createElement("a");
			link.setAttribute("href", blobUrl);
			link.setAttribute("download", "");
			const imgElement = document.createElement("img")
			imgElement.src = blobUrl;
			imgElement.setAttribute("data-image", blobUrl);
			imgElement.addEventListener("click", () => openModal(blobUrl));
			imgElement.classList.add("img");
			imgElement.addEventListener("load", () => adjustImages(imgElement));
			link.appendChild(imgElement);
			gallery.appendChild(link);
		} else if (blobUrl) {
			const link = document.createElement("a");
			link.innerHTML = blobUrl;
			gallery.appendChild(link);
		}
	});

	// Processar vídeos
	data.videos.forEach(async (item) => {
		let blobUrl;
		if (Array.isArray(item.path)) {
			// Se item.path for uma lista, carregar e juntar os arquivos
			const combinedBlob = await fetchAndCombineParts(item.path);
			blobUrl = URL.createObjectURL(combinedBlob);
		} else if (typeof item.path === "string") {
			// Se item.path for uma string, usar diretamente
			blobUrl = item.path;
		}

		if (blobUrl && !blobUrl.includes("iframe")) {
			const videoElement = document.createElement("video");
			videoElement.src = blobUrl;
			videoElement.controls = true; // Adiciona controles de vídeo
			videoElement.style.gridColumn = "span 5"; // Ocupa todas as colunas
			videoElement.style.width = "100%"; // Largura total do container
			videoElement.style.margin = "20px 0"; // Adiciona margem
			videoElement.style.borderRadius = "8px"; // Estilo opcional
			videoElement.style.boxShadow = "0 4px 8px rgba(0, 0, 0, 0.2)"; // Efeito de sombra
			gallery.appendChild(videoElement);
		} else if (blobUrl) {
			const link = document.createElement("div");
			link.innerHTML = blobUrl;
			gallery.appendChild(link);
		}
	});
}


// Função para abrir modal com a imagem clicada
function openModal(imagePath) {
	const modal = document.getElementById("imageModal");
	const modalImage = document.getElementById("modalImage");
	const slideshowBtn = document.getElementById("slideshowBtn");
	let slideshowInterval;

	modalImage.src = imagePath; // Define o caminho da imagem no modal
	modal.classList.add("is-active"); // Abre o modal

	// Fechar o modal
	document.getElementById("closeModal").onclick = () => {
		modal.classList.remove("is-active"); // Fecha o modal
		clearInterval(slideshowInterval); // Para o slideshow
		slideshowBtn.textContent = "Iniciar Slideshow"; // Reseta o botão
		slideshowBtn.disabled = false; // Habilita o botão novamente
	};

	// Iniciar slideshow
	slideshowBtn.onclick = () => {
		if (slideshowBtn.textContent === "Iniciar Slideshow") {
			const images = Array.from(
				document.querySelectorAll(".gallery img")
			).map((img) => img.src);
			let currentIndex = images.indexOf(imagePath); // Começa com a imagem atual

			slideshowBtn.textContent = "Parar Slideshow";
			slideshowBtn.disabled = true; // Desabilita o botão

			slideshowInterval = setInterval(() => {
				currentIndex = (currentIndex + 1) % images.length; // Círculo através das imagens
				modalImage.src = images[currentIndex];
			}, 2000); // Altera a imagem a cada 2 segundos
		} else {
			clearInterval(slideshowInterval);
			slideshowBtn.textContent = "Iniciar Slideshow";
			slideshowBtn.disabled = false; // Habilita o botão novamente
		}
	};
}

function changeColumnCount() {
	let cc = document.getElementById("columnCount").value;
	document.getElementById("gallery").style.columnCount = parseInt(cc);
}

// Chamar a função para carregar imagens quando a página carrega
window.addEventListener("DOMContentLoaded", () => loadImages());
window.addEventListener("load", () => adjustImages());

