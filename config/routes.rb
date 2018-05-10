Rails.application.routes.draw do

  resources :predictions, only: [:index, :show, :new, :create, :destroy]
  get 'error', to: 'predictions#error', as: :error_path
  
end
