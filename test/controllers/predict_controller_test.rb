require 'test_helper'

class PredictControllerTest < ActionDispatch::IntegrationTest
  test "should get new" do
    get predict_new_url
    assert_response :success
  end

  test "should get learn" do
    get predict_learn_url
    assert_response :success
  end

end
