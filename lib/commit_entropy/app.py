#!/usr/bin/env python
# encoding: utf-8

#------------------------------------------------------------------------------
# commit_entropy
# Copyright 2015 Grip QA
# apache
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------------
# c.cmd = Primary command (commit-entropy <primary command>)
# c.cmd2 = Secondary command (commit-entropy <primary command> <secondary command>)
#
# c.arg_to_cmd = first positional argument to the primary command
# c.arg_to_cmd2 = first positional argument to the secondary command
#
# c.option(option_string, [bool argument_required]) = test for option with optional positional argument to option test
# c.option_with_arg(option_string) = test for option and mandatory positional argument to option
# c.flag(flag_string) = test for presence of a "option=argument" style flag
#
# c.arg(arg_string) = returns the next positional argument to the arg_string argument
# c.flag_arg(flag_string) = returns the flag assignment for a "--option=argument" style flag
#------------------------------------------------------------------------------------

# Application start
def main():
    import sys
    from Naked.commandline import Command
    from Naked.toolshed.state import StateObject

    #------------------------------------------------------------------------------------------
    # [ Instantiate command line object ]
    #   used for all subsequent conditional logic in the CLI application
    #------------------------------------------------------------------------------------------
    c = Command(sys.argv[0], sys.argv[1:])
    #------------------------------------------------------------------------------
    # [ Instantiate state object ]
    #------------------------------------------------------------------------------
    state = StateObject()
    #------------------------------------------------------------------------------------------
    # [ Command Suite Validation ] - early validation of appropriate command syntax
    # Test that user entered at least one argument to the executable, print usage if not
    #------------------------------------------------------------------------------------------
    if not c.command_suite_validates():
        from commit_entropy.settings import usage as commit_entropy_usage
        print(commit_entropy_usage)
        sys.exit(1)
    #------------------------------------------------------------------------------------------
    # [ NAKED FRAMEWORK COMMANDS ]
    # Naked framework provides default help, usage, and version commands for all applications
    #   --> settings for user messages are assigned in the lib/commit_entropy/settings.py file
    #------------------------------------------------------------------------------------------
    if c.help():      # User requested commit-entropy help information
        from commit_entropy.settings import help as entropy_help
        print(commit_entropy_help)
        sys.exit(0)
    elif c.usage():   # User requested commit-entropy usage information
        from commit_entropy.settings import usage as commit_entropy_usage
        print(commit_entropy_usage)
        sys.exit(0)
    elif c.version(): # User requested commit-entropy version information
        from commit_entropy.settings import app_name, major_version, minor_version, patch_version
        version_display_string = app_name + ' ' + major_version + '.' + minor_version + '.' + patch_version
        print(version_display_string)
        sys.exit(0)
    #------------------------------------------------------------------------------------------
    # [ PRIMARY COMMAND LOGIC ]
    #   Enter your command line parsing logic below
    #------------------------------------------------------------------------------------------

    # [[ Example usage ]] ------------------------------->>>
    # if c.cmd == 'hello':
    #     if c.cmd2 = 'world':
    # 	      if c.option('--print'):
    # 		      print('Hello World!')
    # elif c.cmd == 'spam':
    #     if c.option_with_arg('--with'):
    # 		  friend_of_spam = c.arg('--with')    # user enters commit-entropy spam --with eggs
    # 		  print('spam and ' + friend_of_spam) # prints 'spam and eggs'
    # elif c.cmd == 'naked':
    #     if c.flag("--language"):
    #         lang = c.flag_arg("--language")     # user enters commit-entropy naked --language=python
    #         print("Naked & " + lang)            # prints 'Naked & python'
    # End example --------------------------------------->>>

    elif c.cmd == 'csv':
        from commit_entropy.commands.csv_printer import CsvPrinter
        printer = CsvPrinter()
        printer.run()

    #------------------------------------------------------------------------------------------
    # [ DEFAULT MESSAGE FOR MATCH FAILURE ]
    #  Message to provide to the user when all above conditional logic fails to meet a true condition
    #------------------------------------------------------------------------------------------
    else:
        print("Could not complete the command that you entered.  Please try again.")
        sys.exit(1) #exit

if __name__ == '__main__':
    main()
