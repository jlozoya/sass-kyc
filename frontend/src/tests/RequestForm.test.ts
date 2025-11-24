import { describe, it, expect } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import RequestForm from '../components/RequestForm.vue'

describe('RequestForm', () => {
  const validPayload = {
    full_name: 'Juan Tester',
    email: 'juan@example.com',
    phone: '5512345678',
    country: 'MX',
    document_type: 'INE',
    document_number: 'ABC123456',
    document_image_url: 'https://example.com/doc.jpg',
    original_document_filename: 'doc.jpg'
  }

  function fillForm(wrapper: ReturnType<typeof mount>) {
    const vm = wrapper.vm as any

    vm.form.full_name = validPayload.full_name
    vm.form.email = validPayload.email
    vm.form.phone = validPayload.phone
    vm.form.country = validPayload.country
    vm.form.document_type = validPayload.document_type
    vm.form.document_number = validPayload.document_number
    vm.form.document_image_url = validPayload.document_image_url
    vm.form.original_document_filename = validPayload.original_document_filename
  }

  it('shows validation errors when submitting an empty form', async () => {
    const wrapper = mount(RequestForm)

    await wrapper.find('form').trigger('submit.prevent')
    await flushPromises()

    const vm = wrapper.vm as any
    expect(vm.errors.length).toBeGreaterThan(0)

    const errorBox = wrapper.find('[class*="bg-rose-50"]')
    expect(errorBox.exists()).toBe(true)
    expect(errorBox.text()).toContain('Por favor corrige los siguientes campos')
  })

  it('emits submit event with payload when form is valid', async () => {
    const wrapper = mount(RequestForm)

    fillForm(wrapper)

    await wrapper.find('form').trigger('submit.prevent')
    await flushPromises()

    const emitted = wrapper.emitted('submit')
    expect(emitted).toBeTruthy()
    expect(emitted!.length).toBe(1)

    const [payload] = emitted![0] as any[]
    expect(payload).toEqual(validPayload)
  })

  it('disables submit button while submitting or uploading', async () => {
    const wrapper = mount(RequestForm)
    const vm = wrapper.vm as any

    vm.submitting = true
    await wrapper.vm.$nextTick()

    const button = wrapper.get('button[type="submit"]')
    expect(button.attributes('disabled')).toBeDefined()
  })
})
