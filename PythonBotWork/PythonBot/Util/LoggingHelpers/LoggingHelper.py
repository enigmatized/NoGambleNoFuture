import logging


def showTradesIn(logger, strategies):
  for strategyName, strategy in strategies.items():
      logger.info("for " + str(strategyName) + "number log_trades_I_decided_to_make" + str( len(strategy['log_trades_I_decided_to_make'])))
      logger.info("for " + str(strategyName) + "number list_of_results_from_orders_this_is_test" + str( len(strategy['list_of_results_from_orders_this_is_test'])))
      logger.info("for " + str(strategyName) + "number list_of_final_stats" + str( len(strategy['list_of_final_stats'])   ))
      
      print("for " + str(strategyName) + "number log_trades_I_decided_to_make" + str( len(strategy['log_trades_I_decided_to_make'])))
      print("for " + str(strategyName) + "number list_of_results_from_orders_this_is_test" + str( len(strategy['list_of_results_from_orders_this_is_test'])))
      print("for " + str(strategyName) + "number list_of_final_stats" + str( len(strategy['list_of_final_stats'])   ))
