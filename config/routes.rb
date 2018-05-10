Rails.application.routes.draw do
  #get 'new', to: 'predict#new'
  #post 'learn', to: 'predict#learn'
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
  resources :predictions, only [:index, :show, :new, :create, :destroy]
end
