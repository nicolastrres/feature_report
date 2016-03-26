def get_feature(file_lines):
    feature_label = 'Feature:'
    for line in file_lines:
        if feature_label in line:
            return line[:-1]


def get_scenarios(file_lines):
    scenario_label = 'Scenario:'
    file_lines = _remove_spaces_in_lines(file_lines)
    scenarios_start_line_number = _get_first_line_number_of_each_scenario(file_lines, scenario_label)
    return _create_list_of_scenarios(file_lines, scenarios_start_line_number)


def _create_list_of_scenarios(file_lines, scenarios_start_line_number):
    scenarios = []
    for index, start_line_number in enumerate(scenarios_start_line_number):
        if _is_not_last_scenario(index, scenarios_start_line_number):
            scenarios.append(
                _get_lines_between_start_and_end_line_number(
                    file_lines,
                    start_line_number,
                    _next_scenario_start_line_number(index, scenarios_start_line_number))
            )
        else:
            scenarios.append(_get_lines_between_start_and_end_line_number(file_lines, start_line_number))
    return scenarios


def _is_not_last_scenario(index, scenarios):
    return index + 1 < len(scenarios)


def _next_scenario_start_line_number(index, scenarios_start_line_number):
    return scenarios_start_line_number[index+1]


def _get_first_line_number_of_each_scenario(file_lines, scenario_label):
    scenarios_start_line_number = []
    for line in file_lines:
        if scenario_label in line:
            scenarios_start_line_number.append(file_lines.index(line))

    return scenarios_start_line_number


def _get_lines_between_start_and_end_line_number(file_lines, start_line, last_line=None):
    scenario_lines = file_lines[start_line: last_line]
    string_scenario = ''.join(scenario_lines)
    return string_scenario


def _remove_spaces_in_lines(file_lines):
    return [line.lstrip(' ') for line in file_lines]
