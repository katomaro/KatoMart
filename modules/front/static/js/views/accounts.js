const { ref, onMounted, watch } = Vue
import { convertUnixTimestampToDate } from "../utils.js"


export default {
  async setup() {
    const form = ref({
      platform_id: "",
      username: "",
      password: "",
    })

    const message = ref("")
    const platforms = ref([])
    const accounts = ref([])

    onMounted(async () => {
      const res = await fetch('/api/platforms')
      platforms.value = await res.json()
    })

    const fetchAccounts = async (platformId) => {
      const res = await fetch(`/api/get_accounts?platform_id=${platformId}`)
      const data = await res.json()
      accounts.value = data.map(a => ({ ...a, selected: false }))
    }

    watch(() => form.value.platform_id, async (newPlatformId) => {
      await fetchAccounts(newPlatformId)
    })

    const handleSubmit = async () => {
      const res = await fetch('/api/accounts', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(form.value)
      })

      const data = await res.json()
      if (data.success) {
        message.value = "Conta Adicionada com Sucesso!"
        form.value.username = ""
        form.value.password = ""
        await fetchAccounts(form.value.platform_id)
      } else {
        message.value = "Falha ao salvar a conta."
      }
    }

    const toggleAccount = (accountId) => {
      const account = accounts.value.find(a => a.id === accountId)
      if (account.selected) {
        accounts.value = accounts.value.map(a => ({ ...a, selected: false }))
      } else {
        accounts.value = accounts.value.map(a => (a.id === account.id ? { ...a, selected: true } : { ...a, selected: false }))
      }
    }

    const deleteAccount = async (accountId) => {
      const res = await fetch(`/api/delete_account`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ account_id: accountId })
      })
      if (res.ok) {
        message.value = "Conta Removida com Sucesso!"
        await fetchAccounts(form.value.platform_id)
      }
    }

    const initializeAccount = async (account) => {
      await fetch(`/api/select_account`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ account_id: account.id, platform_id: account.platform_id })
      })

      fetchAccounts(form.value.platform_id)
    }


    return { form, platforms, accounts, message, handleSubmit, toggleAccount, deleteAccount, convertUnixTimestampToDate, initializeAccount }
  },
  template: `
  <h1 class="text-2xl font-bold text-center mb-8">
      <i class="fa-solid fa-users"></i> Gerenciar Contas das Plataformas
  </h1>
  <div class="flex flex-col items-center min-h-screen">
    <div v-if="message" class="alert alert-info shadow-lg mb-6 w-1/2">
      {{ message }}
    </div>

    <form class="max-w-lg w-full bg-base-100 shadow-xl rounded-lg p-4 border-2 border-primary" @submit.prevent="handleSubmit">
      <div class="form-group mb-4">
        <label for="platformSelect" class="label">
          <span class="label-text font-semibold">Plataforma:</span>
        </label>
        <select class="input input-bordered w-full" v-model="form.platform_id">
          <option value="" disabled selected>Selecione uma plataforma</option>
          <option v-for="platform in platforms" :value="platform[0]">{{ platform[1] }}</option>
        </select>
      </div>
      <div v-if="form.platform_id">
        <div class="form-group mb-4">
          <label for="username" class="label">
            <span class="label-text font-semibold">Email:</span>
          </label>
          <input type="email" id="username" class="input input-bordered w-full" v-model="form.username" required>
        </div>
        <div class="form-group mb-6">
          <label for="password" class="label">
            <span class="label-text font-semibold">Senha:</span>
          </label>
          <input type="password" id="password" class="input input-bordered w-full" v-model="form.password" required>
        </div>
          <button class="btn btn-primary w-full">Salvar Conta</button>
      </div>
    </form>

    <table class="table table-zebra my-8 w-1/2" v-if="accounts.length > 0">
      <thead class="text-center">
        <tr>
          <th class="px-5 py-3 border-b-2 border-gray-200 bg-base-100 font-semibold uppercase">Selecionar</th>
          <th class="px-5 py-3 border-b-2 border-gray-200 bg-base-100 font-semibold uppercase">Ativa?</th>
          <th class="px-5 py-3 border-b-2 border-gray-200 bg-base-100 font-semibold uppercase">Usuário</th>
          <th class="px-5 py-3 border-b-2 border-gray-200 bg-base-100 font-semibold uppercase">Senha</th>
          <th class="px-5 py-3 border-b-2 border-gray-200 bg-base-100 font-semibold uppercase">Token</th>
          <th class="px-5 py-3 border-b-2 border-gray-200 bg-base-100 font-semibold uppercase">Expiração do Token</th>
          <th class="px-5 py-3 border-b-2 border-gray-200 bg-base-100 font-semibold uppercase">Revalidar Token</th>
          <th class="px-5 py-3 border-b-2 border-gray-200 bg-base-100 font-semibold uppercase">Deletar</th>
        </tr>
      </thead>
      <tbody class="text-center">
          <tr v-for="account in accounts">
            <td class="px-5 py-5 border-b border-gray-200 whitespace-nowrap">
              <input type="checkbox" class="checkbox checkbox-primary" @change="toggleAccount(account.id)" :checked="account.selected" />
            </td>
            <td class="px-5 py-5 border-b border-gray-200 whitespace-nowrap">
              {{ account.is_active ? 'Sim' : 'Não' }}
            </td>
            <td class="px-5 py-5 border-b border-gray-200 whitespace-nowrap">
              {{ account.username }}
            </td>
            <td class="px-5 py-5 border-b border-gray-200 whitespace-nowrap">
              {{ account.password || 'N/A' }}
            </td>
            <td class="px-5 py-5 border-b border-gray-200 whitespace-nowrap">
              <input type="text" class="input input-bordered w-full mx-5 px-0.5" :value="account.auth_token">
            </td>
            <td class="px-5 py-5 border-b border-gray-200 whitespace-nowrap">
              {{ account.auth_token_expires_at && convertUnixTimestampToDate(account.auth_token_expires_at) || 'N/A' }}
            </td>
            <td class="px-5 py-5 border-b border-gray-200 whitespace-nowrap">
              <button class="btn btn-primary btn-sm">Revalidar Token</button>
            </td>
            <td class="px-5 py-5 border-b border-gray-200 whitespace-nowrap">
              <button class="btn btn-error btn-sm" @click="deleteAccount(account.id)">Deletar</button>
            </td>
          </tr>
      </tbody>
    </table>

    <button class="btn btn-primary" v-if="accounts.some(x => x.selected)" @click="initializeAccount(accounts.find(x => x.selected))">Inicializar Conta Selecionada</button>
  </div>
  `
}