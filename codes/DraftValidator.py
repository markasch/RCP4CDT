
schema = {
  "title": "Workflow Scheduling Input",
  "description": "Input specification for multi-mode resource-constrained project scheduling (MM-RCPSP)",
  "type": "object",
  
  "properties": {
    "problem_name": {
      "type": "string",
      "description": "Optional identifier for the problem instance"
    },
    
    "horizon": {
      "type": "integer",
      "minimum": 1,
      "description": "Planning horizon (maximum time periods)"
    },
    
    "resources": {
      "type": "array",
      "description": "Available renewable resources",
      "minItems": 1,
      "items": { "$ref": "#/$defs/resource" },
      "uniqueItems": true
    },
    
    "jobs": {
      "type": "array",
      "description": "Jobs to be scheduled",
      "minItems": 1,
      "items": { "$ref": "#/$defs/job" },
      "uniqueItems": true
    },
    
    "modes": {
      "type": "array",
      "description": "Execution modes for jobs",
      "minItems": 1,
      "items": { "$ref": "#/$defs/mode" },
      "uniqueItems": true
    },
    
    "precedences": {
      "type": "array",
      "description": "Precedence constraints defining the DAG",
      "items": { "$ref": "#/$defs/precedence" },
      "default": []
    }
  },
  
  "required": ["resources", "jobs", "modes"],
  "additionalProperties": false,
  
  "$defs": {
    "resource": {
      "type": "object",
      "title": "Resource",
      "description": "A renewable resource with per-period capacity",
      "properties": {
        "resource_id": {
          "type": "string",
          "minLength": 1,
          "pattern": "^[A-Za-z_][A-Za-z0-9_]*$",
          "description": "Unique identifier (alphanumeric with underscores, starting with letter)"
        },
        "name": {
          "type": "string",
          "description": "Human-readable name"
        },
        "capacity": {
          "type": "integer",
          "minimum": 0,
          "description": "Maximum units available per time period"
        }
      },
      "required": ["resource_id", "capacity"],
      "additionalProperties": false
    },
    
    "job": {
      "type": "object",
      "title": "Job",
      "description": "A unit of work to be scheduled",
      "properties": {
        "job_id": {
          "type": "string",
          "minLength": 1,
          "pattern": "^[A-Za-z_][A-Za-z0-9_]*$",
          "description": "Unique identifier"
        },
        "name": {
          "type": "string",
          "description": "Human-readable name"
        },
        "release_time": {
          "type": "integer",
          "minimum": 0,
          "default": 0,
          "description": "Earliest time the job may start"
        },
        "deadline": {
          "type": ["integer", "null"],
          "minimum": 0,
          "default": null,
          "description": "Latest time by which the job must finish (null = no deadline)"
        }
      },
      "required": ["job_id"],
      "additionalProperties": false
    },
    
    "mode": {
      "type": "object",
      "title": "Mode",
      "description": "An execution mode for a job specifying duration, cost, and resource needs",
      "properties": {
        "mode_id": {
          "type": "string",
          "minLength": 1,
          "pattern": "^[A-Za-z_][A-Za-z0-9_]*$",
          "description": "Unique identifier for this mode"
        },
        "job_id": {
          "type": "string",
          "minLength": 1,
          "description": "Reference to the parent job"
        },
        "duration": {
          "type": "integer",
          "minimum": 0,
          "description": "Processing time in periods"
        },
        "cost": {
          "type": "number",
          "minimum": 0,
          "description": "Cost of selecting this mode"
        },
        "resource_requirements": {
          "type": "array",
          "description": "Resources consumed while executing in this mode",
          "items": { "$ref": "#/$defs/resource_requirement" },
          "default": []
        }
      },
      "required": ["mode_id", "job_id", "duration", "cost"],
      "additionalProperties": false
    },
    
    "resource_requirement": {
      "type": "object",
      "title": "Resource Requirement",
      "description": "Demand for a specific resource during job execution",
      "properties": {
        "resource_id": {
          "type": "string",
          "minLength": 1,
          "description": "Reference to a defined resource"
        },
        "demand": {
          "type": "integer",
          "minimum": 0,
          "description": "Units required per period while the job executes"
        }
      },
      "required": ["resource_id", "demand"],
      "additionalProperties": false
    },
    
    "precedence": {
      "type": "object",
      "title": "Precedence Constraint",
      "description": "A directed edge in the job DAG",
      "properties": {
        "predecessor": {
          "type": "string",
          "minLength": 1,
          "description": "job_id of the job that must finish first"
        },
        "successor": {
          "type": "string",
          "minLength": 1,
          "description": "job_id of the job that must start after"
        },
        "lag": {
          "type": "integer",
          "minimum": 0,
          "default": 0,
          "description": "Minimum time gap between predecessor finish and successor start"
        }
      },
      "required": ["predecessor", "successor"],
      "additionalProperties": false
    }
  }
}