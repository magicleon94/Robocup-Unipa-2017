from States import States

states_manager = States()

print "Initial state:\t", states_manager.get_targets()

while None not in states_manager.get_targets():
    states_manager.state_transition()
    print states_manager.get_targets()

print "Final state reached!"

states_manager.set_state("object", "yellow")

print "New initial state:\t", states_manager.get_targets()

while None not in states_manager.get_targets():
    states_manager.state_transition()
    print states_manager.get_targets()

print "Final state reached!"
