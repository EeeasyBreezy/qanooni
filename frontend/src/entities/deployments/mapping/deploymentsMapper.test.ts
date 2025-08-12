import { describe, expect, it } from 'vitest'
import { deploymentDTOToDeployment } from './deploymentsMapper'
import type { DeploymentDTO } from '../dto/DeploymentDTO'

describe('deploymentDTOToDeployment', () => {
  it('maps all fields 1:1', () => {
    const dto: DeploymentDTO = {
      id: 'dep-1',
      name: 'My Deployment',
      description: 'Description',
      createdAt: '2024-01-01T00:00:00.000Z',
      updatedAt: '2024-01-02T00:00:00.000Z',
    }

    const model = deploymentDTOToDeployment(dto)

    expect(model).toEqual({
      id: 'dep-1',
      name: 'My Deployment',
      description: 'Description',
      createdAt: '2024-01-01T00:00:00.000Z',
      updatedAt: '2024-01-02T00:00:00.000Z',
    })
  })

  it('preserves empty strings and values', () => {
    const dto: DeploymentDTO = {
      id: '',
      name: '',
      description: '',
      createdAt: '',
      updatedAt: '',
    }

    const model = deploymentDTOToDeployment(dto)

    expect(model).toEqual({
      id: '',
      name: '',
      description: '',
      createdAt: '',
      updatedAt: '',
    })
  })
})


