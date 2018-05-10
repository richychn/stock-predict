class CreatePredictions < ActiveRecord::Migration[5.2]
  def change
    create_table :predictions do |t|
      t.string :ticker
      t.string :model
      t.float :confidence
      t.integer :result

      t.timestamps
    end
  end
end
