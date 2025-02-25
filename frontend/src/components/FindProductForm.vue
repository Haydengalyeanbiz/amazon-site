<template>
	<div class="find-product-form-container">
		<h1>Find Amazon Product</h1>
		<form
			v-if="!product || !product.title"
			@submit.prevent="fetchProductDetails"
			class="fetch-form"
		>
			<div>
				<label for="affiliate-link">Affiliate Link:</label>
				<input
					type="text"
					v-model="affiliateLink"
					id="affiliate-link"
					placeholder="Paste your Amazon affiliate link here"
					required
				/>
			</div>
			<button
				class="fetch-product-btn"
				type="submit"
			>
				Fetch Product Details
			</button>
		</form>

		<div class="preview-form-structure">
			<div
				class="preview-post-structure"
				v-if="postForm.title"
			>
				<div class="top-preview">
					<img
						class="preview-img"
						:src="postForm.imageUrl || ''"
						alt="Product Image"
					/>
					<p class="preview-title">{{ postForm.title || '' }}</p>
				</div>
				<div class="bottom-preview">
					<p class="preview-description">{{ postForm.description || '' }}</p>
					<p class="preview-price">{{ postForm.price || '' }}</p>
				</div>
			</div>
			<form
				v-if="product && product.title"
				@submit.prevent="submitForm"
				class="add-post-form"
			>
				<div>
					<label for="title">Title:</label>
					<input
						type="text"
						id="title"
						v-model="postForm.title"
						:placeholder="product?.title || ''"
						required
					/>
				</div>

				<div>
					<label for="price">Price:</label>
					<input
						type="text"
						id="price"
						v-model="postForm.price"
						:placeholder="product?.price || 'Price unavailable'"
						required
					/>
				</div>

				<div>
					<label for="description">Description:</label>
					<textarea
						id="description"
						v-model="postForm.description"
						placeholder="Product Description"
						required
					></textarea>
				</div>

				<div>
					<label for="image">Image URL: DON'T CHANGE!</label>
					<input
						type="text"
						id="image"
						v-model="postForm.imageUrl"
						:placeholder="product?.imageUrl || ''"
						required
					/>
				</div>

				<div>
					<label for="link">Product Link: DON'T CHANGE!</label>
					<input
						type="text"
						id="link"
						v-model="affiliateLink"
						required
					/>
				</div>

				<button
					class="submit-btn"
					type="submit"
				>
					Submit Post
				</button>
			</form>

			<p v-if="error">{{ error }}</p>
		</div>
	</div>
</template>

<script>
import axios from 'axios';
import { mapActions } from 'vuex';

export default {
	data() {
		return {
			affiliateLink: '',
			product: {},
			error: null,
			postForm: {
				title: '',
				price: '',
				description: '',
				imageUrl: '',
			},
		};
	},
	methods: {
		...mapActions(['submitPost']),
		extractASIN(affiliateLink) {
			const regex = /([A-Z0-9]{10})(?:[/?]|$)/;
			const match = affiliateLink.match(regex);
			return match ? match[1] : null;
		},
		async fetchProductDetails() {
			this.error = null;
			this.product = null;

			const asin = this.extractASIN(this.affiliateLink);
			if (!asin) {
				this.error = 'Invalid Amazon link. Could not extract ASIN.';
				return;
			}

			try {
				const response = await axios.post('/amazon/fetch-product-details', {
					asin,
				});
				this.product = response.data;

				this.postForm.title = this.product?.title || '';
				this.postForm.price = this.product?.price || 'Price unavailable';
				this.postForm.imageUrl = this.product?.imageUrl || '';
			} catch (error) {
				console.error('Failed to fetch product details:', error);
				this.error = 'Failed to fetch product details. Please try again.';
			}
		},
		// Vuex Action: submitPost
		async submitPost({ state }, postData) {
			console.log(this.$store.state);
			console.log('isAuthenticated:', state.isAuthenticated);
			if (!state.isAuthenticated) {
				throw new Error('User is not authenticated');
			}
			try {
				console.log('This is the payload', postData);
				const response = await axios.post('/api/submit-post', postData);
				return response.data;
			} catch (error) {
				console.error('Failed to submit post:', error);
				throw error;
			}
		},
		async submitForm() {
			try {
				await this.$store.dispatch('submitPost', {
					title: this.postForm.title || '', // Default to empty strings if undefined
					price: this.postForm.price || '',
					description: this.postForm.description || '',
					image_url: this.postForm.imageUrl || '',
					link_url: this.affiliateLink || '',
				});
				this.$router.push('/');
			} catch (error) {
				console.error('Error submitting post:', error);
				this.error = 'Failed to submit post. Please try again.';
			}
		},
	},
};
</script>

<style>
.find-product-form-container {
	position: relative;
	padding-top: 8dvh;
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 1rem;
	height: auto;
	background-color: var(--primary-light);
}

.fetch-form {
	display: flex;
	flex-direction: column;
	gap: 1rem;
}

.preview-form-structure {
	display: flex;
	justify-content: space-evenly;
	gap: 3rem;
	padding: 1rem 0;
}

.preview-post-structure {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 1rem;
	height: auto;
	width: 404px;
	gap: 1rem;
	color: var(--primary-light);
	border-radius: 12px;
	background-color: var(--primary-dark);
}

.top-preview {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 1rem;
}

.bottom-preview {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 1rem;
	padding: 0 1rem 1rem;
}

.preview-post-structure p {
	margin: 0;
	padding: 0;
}

.preview-title {
	max-width: 350px;
	padding: 0;
	margin: 0;
	font-family: var(--header-ff);
	font-size: var(--fs-medium);
}

.preview-img {
	width: 400px;
	height: 400px;
	object-fit: cover;
	object-position: center;
	border-radius: 12px;
	border: solid 4px var(--secondary-dark);
}

.add-post-form {
	display: flex;
	flex-direction: column;
	gap: 1rem;
}

.add-post-form div {
	display: flex;
	flex-direction: column;
}

.add-post-form input {
	width: 500px;
}

.add-post-form textarea {
	max-width: 500px;

	max-height: 150px;
}

@media (max-width: 780px) {
	.preview-form-structure {
		flex-direction: column;
		gap: 0;
	}

	.add-post-form {
		width: 80%;
	}

	.add-post-form input {
		width: 400px;
	}
}
</style>
