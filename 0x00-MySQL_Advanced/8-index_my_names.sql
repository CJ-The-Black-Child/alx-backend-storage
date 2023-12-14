-- This script creates an index on the first letter of the 'name' 
-- field in the 'names' table
CREATE INDEX idx_name_first ON names(LEFT(name, 1));
